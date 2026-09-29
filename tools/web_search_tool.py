from urllib.parse import (
    quote_plus,
    unquote,
    urlparse,
    parse_qs
)

from urllib.request import (
    Request,
    urlopen
)

from urllib.error import (
    URLError,
    HTTPError
)

from playwright.sync_api import (
    sync_playwright,
    TimeoutError as PlaywrightTimeoutError
)


class WebSearchTool:

    name = "web_search"

    description = (
        "Safely searches the web and returns a limited set "
        "of search result titles, URLs, and descriptions."
    )

    MAX_QUERY_LENGTH = 500

    MAX_RESULTS = 5

    REQUEST_TIMEOUT = 10

    USER_AGENT = (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/142.0 Safari/537.36"
    )

    def execute(
        self,
        query,
        max_results=None
    ):

        # -----------------------------------------
        # VALIDATE QUERY
        # -----------------------------------------

        if query is None:

            raise ValueError(
                "Search query cannot be empty."
            )

        query = str(
            query
        ).strip()

        if not query:

            raise ValueError(
                "Search query cannot be empty."
            )

        if len(query) > self.MAX_QUERY_LENGTH:

            raise ValueError(
                "Search query is too long. "
                "Maximum length is 500 characters."
            )

        # -----------------------------------------
        # VALIDATE RESULT COUNT
        # -----------------------------------------

        if max_results is None:

            selected_results = self.MAX_RESULTS

        else:

            try:

                selected_results = int(
                    max_results
                )

            except (
                TypeError,
                ValueError
            ) as error:

                raise ValueError(
                    "Maximum results must be an integer."
                ) from error

        if selected_results < 1:

            raise ValueError(
                "Maximum results must be at least 1."
            )

        if selected_results > self.MAX_RESULTS:

            selected_results = self.MAX_RESULTS

        # -----------------------------------------
        # BUILD SEARCH URL
        # -----------------------------------------

        encoded_query = quote_plus(
            query
        )

        search_url = (
            "https://www.google.com/search"
            f"?q={encoded_query}"
            "&hl=en"
        )

        request = Request(
            search_url,
            headers={
                "User-Agent": self.USER_AGENT,
                "Accept-Language": "en-US,en;q=0.9"
            }
        )

        # -----------------------------------------
        # PRIMARY HTTP REQUEST
        # -----------------------------------------

        try:

            with urlopen(
                request,
                timeout=self.REQUEST_TIMEOUT
            ) as response:

                html = response.read().decode(
                    "utf-8",
                    errors="replace"
                )

        except HTTPError as error:

            raise RuntimeError(
                "Web search request failed "
                f"with HTTP status {error.code}."
            ) from error

        except URLError as error:

            raise RuntimeError(
                "Unable to connect to the web."
            ) from error

        except TimeoutError as error:

            raise RuntimeError(
                "Web search request timed out."
            ) from error

        except OSError as error:

            raise RuntimeError(
                "Web search request failed."
            ) from error

        # -----------------------------------------
        # TRY HTTP PARSER FIRST
        # -----------------------------------------

        results = self._parse_results(
            html,
            selected_results
        )

        if results:

            return results

        # -----------------------------------------
        # GOOGLE REQUIRES JAVASCRIPT
        # -----------------------------------------

        return self._search_with_browser(
            search_url,
            selected_results
        )

    # =================================================
    # BROWSER SEARCH
    # =================================================

    def _search_with_browser(
        self,
        search_url,
        max_results
    ):

        results = []

        try:

            with sync_playwright() as playwright:

                browser = playwright.chromium.launch(
                    headless=True
                )

                try:

                    context = browser.new_context(
                        user_agent=self.USER_AGENT,
                        locale="en-US",
                        viewport={
                            "width": 1366,
                            "height": 768
                        }
                    )

                    page = context.new_page()

                    page.goto(
                        search_url,
                        wait_until="domcontentloaded",
                        timeout=self.REQUEST_TIMEOUT * 1000
                    )

                    # -----------------------------------------
                    # WAIT FOR GOOGLE RESULTS
                    # -----------------------------------------

                    try:

                        page.wait_for_selector(
                            "h3",
                            timeout=5000
                        )

                    except PlaywrightTimeoutError:

                        pass

                    # -----------------------------------------
                    # EXTRACT RESULTS
                    # -----------------------------------------

                    headings = page.locator(
                        "h3"
                    )

                    count = headings.count()

                    for index in range(count):

                        if len(results) >= max_results:

                            break

                        heading = headings.nth(
                            index
                        )

                        try:

                            title = heading.inner_text(
                                timeout=2000
                            ).strip()

                        except Exception:

                            continue

                        if not title:

                            continue

                        # -----------------------------------------
                        # FIND ANCHOR
                        # -----------------------------------------

                        link = heading.locator(
                            "xpath=ancestor::a[1]"
                        )

                        if link.count() == 0:

                            link = heading.locator(
                                "xpath=ancestor::div[1]//a[1]"
                            )

                        if link.count() == 0:

                            continue

                        try:

                            url = link.first.get_attribute(
                                "href",
                                timeout=2000
                            )

                        except Exception:

                            continue

                        if not url:

                            continue

                        url = self._clean_url(
                            url
                        )

                        if not self._is_valid_url(
                            url
                        ):

                            continue

                        # -----------------------------------------
                        # SKIP DUPLICATES
                        # -----------------------------------------

                        duplicate = False

                        for existing in results:

                            if existing["url"] == url:

                                duplicate = True

                                break

                        if duplicate:

                            continue

                        results.append(
                            {
                                "title": title,
                                "url": url
                            }
                        )

                    context.close()

                finally:

                    browser.close()

        except PlaywrightTimeoutError as error:

            raise RuntimeError(
                "Web search request timed out."
            ) from error

        except Exception as error:

            raise RuntimeError(
                "Browser-based web search failed."
            ) from error

        return results

    # =================================================
    # PARSE HTTP RESULTS
    # =================================================

    def _parse_results(
        self,
        html,
        max_results
    ):

        results = []

        position = 0

        while (
            position < len(html)
            and len(results) < max_results
        ):

            # -----------------------------------------
            # FIND NEXT H3
            # -----------------------------------------

            title_start = html.find(
                "<h3",
                position
            )

            if title_start == -1:

                break

            title_open = html.find(
                ">",
                title_start
            )

            if title_open == -1:

                break

            title_close = html.find(
                "</h3>",
                title_open
            )

            if title_close == -1:

                break

            title = html[
                title_open + 1:
                title_close
            ]

            title = self._clean_html(
                title
            )

            # -----------------------------------------
            # FIND RESULT URL
            # -----------------------------------------

            url = self._find_result_url(
                html,
                title_start,
                title_close,
                position
            )

            # -----------------------------------------
            # VALIDATE RESULT
            # -----------------------------------------

            if (
                title
                and url
                and self._is_valid_url(url)
            ):

                duplicate = False

                for existing in results:

                    if existing["url"] == url:

                        duplicate = True

                        break

                if not duplicate:

                    results.append(
                        {
                            "title": title,
                            "url": url
                        }
                    )

            position = (
                title_close
                + len("</h3>")
            )

        return results

    # =================================================
    # FIND RESULT URL
    # =================================================

    def _find_result_url(
        self,
        html,
        title_start,
        title_close,
        result_start
    ):

        # -----------------------------------------
        # CASE 1:
        # <a href="URL"><h3>Title</h3></a>
        # -----------------------------------------

        previous_anchor_start = html.rfind(
            "<a ",
            result_start,
            title_start
        )

        if previous_anchor_start != -1:

            previous_anchor_close = html.rfind(
                "</a>",
                result_start,
                title_start
            )

            if (
                previous_anchor_close == -1
                or previous_anchor_close
                < previous_anchor_start
            ):

                anchor_end = html.find(
                    ">",
                    previous_anchor_start,
                    title_start
                )

                if anchor_end != -1:

                    url = self._extract_href(
                        html[
                            previous_anchor_start:
                            anchor_end
                        ]
                    )

                    if url:

                        return self._clean_url(
                            url
                        )

        # -----------------------------------------
        # CASE 2:
        # <h3>Title</h3>
        # <a href="URL">
        # -----------------------------------------

        next_div_end = html.find(
            "</div>",
            title_close
        )

        if next_div_end == -1:

            next_div_end = len(html)

        following_anchor_start = html.find(
            "<a ",
            title_close,
            next_div_end
        )

        if following_anchor_start != -1:

            anchor_end = html.find(
                ">",
                following_anchor_start,
                next_div_end
            )

            if anchor_end != -1:

                url = self._extract_href(
                    html[
                        following_anchor_start:
                        anchor_end
                    ]
                )

                if url:

                    return self._clean_url(
                        url
                    )

        # -----------------------------------------
        # CASE 3:
        # NEARBY FALLBACK
        # -----------------------------------------

        nearby_start = max(
            0,
            title_start - 2000
        )

        nearby_end = min(
            len(html),
            title_close + 2000
        )

        nearby = html[
            nearby_start:
            nearby_end
        ]

        href_position = nearby.find(
            'href="'
        )

        if href_position != -1:

            href_position += len(
                'href="'
            )

            href_end = nearby.find(
                '"',
                href_position
            )

            if href_end != -1:

                url = nearby[
                    href_position:
                    href_end
                ]

                return self._clean_url(
                    url
                )

        return ""

    # =================================================
    # EXTRACT HREF
    # =================================================

    @staticmethod
    def _extract_href(
        value
    ):

        href_start = value.find(
            'href="'
        )

        if href_start == -1:

            return ""

        href_start += len(
            'href="'
        )

        href_end = value.find(
            '"',
            href_start
        )

        if href_end == -1:

            return ""

        return value[
            href_start:
            href_end
        ]

    # =================================================
    # CLEAN URL
    # =================================================

    @staticmethod
    def _clean_url(
        url
    ):

        url = (
            url
            .replace(
                "&amp;",
                "&"
            )
            .strip()
        )

        # -----------------------------------------
        # GOOGLE REDIRECT URL
        # -----------------------------------------

        if url.startswith(
            "/url?"
        ):

            parsed = urlparse(
                url
            )

            query = parse_qs(
                parsed.query
            )

            target = query.get(
                "q"
            )

            if target:

                return unquote(
                    target[0]
                )

            target = query.get(
                "url"
            )

            if target:

                return unquote(
                    target[0]
                )

        # -----------------------------------------
        # PROTOCOL-RELATIVE URL
        # -----------------------------------------

        if url.startswith(
            "//"
        ):

            return (
                "https:"
                + url
            )

        return url

    # =================================================
    # VALIDATE URL
    # =================================================

    @staticmethod
    def _is_valid_url(
        url
    ):

        if not url:

            return False

        if not (
            url.startswith(
                "http://"
            )
            or url.startswith(
                "https://"
            )
        ):

            return False

        parsed = urlparse(
            url
        )

        if not parsed.netloc:

            return False

        return True

    # =================================================
    # CLEAN HTML
    # =================================================

    @staticmethod
    def _clean_html(
        value
    ):

        replacements = {
            "&amp;": "&",
            "&quot;": '"',
            "&#39;": "'",
            "&lt;": "<",
            "&gt;": ">",
            "&#x27;": "'",
            "&#x2F;": "/",
            "&nbsp;": " "
        }

        for (
            source,
            target
        ) in replacements.items():

            value = value.replace(
                source,
                target
            )

        while (
            "<" in value
            and ">" in value
        ):

            start = value.find(
                "<"
            )

            end = value.find(
                ">",
                start
            )

            if end == -1:

                break

            value = (
                value[:start]
                + value[end + 1:]
            )

        return " ".join(
            value.split()
        )
class ToolRegistry:

    def __init__(self):

        self.tools = {}

    def register(self, name, tool):

        if not name:
            raise ValueError(
                "Tool name cannot be empty."
            )

        name = str(name).strip().lower()

        if not name:
            raise ValueError(
                "Tool name cannot be empty."
            )

        if tool is None:
            raise ValueError(
                f"Tool cannot be None: {name}"
            )

        if name in self.tools:
            raise ValueError(
                f"Tool already registered: {name}"
            )

        self.tools[name] = tool

        return True

    def get(self, name):

        if not name:
            return None

        name = str(name).strip().lower()

        return self.tools.get(name)

    def exists(self, name):

        return self.get(name) is not None

    def unregister(self, name):

        if not name:
            return False

        name = str(name).strip().lower()

        if name not in self.tools:
            return False

        del self.tools[name]

        return True

    def list_tools(self):

        return list(self.tools.keys())

    def get_definitions(self):

        definitions = []

        for name, tool in self.tools.items():

            definition = {
                "name": name,
                "description": getattr(
                    tool,
                    "description",
                    ""
                )
            }

            definitions.append(definition)

        return definitions

    def count(self):

        return len(self.tools)

    def clear(self):

        self.tools.clear()
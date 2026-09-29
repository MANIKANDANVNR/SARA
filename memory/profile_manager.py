class ProfileManager:

    def __init__(self):

        self.profile = {}

    # -------------------------------------------------
    # PROFILE
    # -------------------------------------------------

    def set(self, key, value):

        if not key or value is None:

            return False

        key = str(key).strip().lower()

        if not key:

            return False

        self.profile[key] = value

        return True

    def get(self, key, default=None):

        if not key:

            return default

        return self.profile.get(
            str(key).strip().lower(),
            default
        )

    def remove(self, key):

        if not key:

            return False

        key = str(key).strip().lower()

        if key not in self.profile:

            return False

        del self.profile[key]

        return True

    def get_all(self):

        return dict(self.profile)

    def load(self, profile):

        if not isinstance(profile, dict):

            self.profile = {}

            return False

        self.profile = dict(profile)

        return True

    def clear(self):

        self.profile.clear()

    def is_empty(self):

        return len(self.profile) == 0

    def count(self):

        return len(self.profile)
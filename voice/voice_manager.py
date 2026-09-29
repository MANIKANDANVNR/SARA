class VoiceManager:

    def __init__(self):

        self.available = False

    def initialize(self):

        self.available = False

    def listen(self):

        if not self.available:
            return ""

        return ""

    def speak(self, text):

        if not self.available:
            return False

        return True
class TerminalUI:

    def display_banner(self):

        print()
        print("=" * 60)
        print("                         SARA")
        print("              PERSONAL AI ASSISTANT")
        print("=" * 60)
        print()

    def show_message(self, message):

        print(f"SARA: {message}")

    def get_input(self):

        try:

            return input("\nYou: ").strip()

        except KeyboardInterrupt:

            print()
            return "shutdown"

        except EOFError:

            return "shutdown"
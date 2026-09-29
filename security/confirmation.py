class ConfirmationManager:

    def request_confirmation(self, message):

        print()
        print("SECURITY CONFIRMATION")
        print("---------------------")
        print(message)

        answer = input(
            "Confirm? [yes/no]: "
        ).strip().lower()

        return answer in {
            "yes",
            "y"
        }
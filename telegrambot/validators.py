from re import fullmatch


class EmailValidators:

    @staticmethod
    def check_correct_email(email):
        if not fullmatch(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', email):
            return True
        return False



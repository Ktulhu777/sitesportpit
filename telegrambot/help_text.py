class SuccessEmail:
    def __init__(self, email, nickname, user_id, *args, **kwargs):
        self._email = email
        self._nickname = nickname
        self.__user_id = user_id
        self.args = args
        self.kwargs = kwargs

    def get_letter(self):
        return f"""
        Здраствуйте {self._nickname}, Вы указали боту Email {self._email}.
        Для привязки вашего профиля к боту перейдите по ссылке: - 
        http://127.0.0.1:8000/api/{self.__user_id}/
        Если вы этого не делали проигнорируйте это сообщение.
        """

    @property
    def email(self):
        return self._email

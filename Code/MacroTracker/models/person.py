class Person:
    def __init__(self, username, password):
        self._username = username
        self._password = password

    def get_username(self):
        return self._username

from abc import ABC, abstractmethod

class Person(ABC):   # ABSTRACTION

    def __init__(self, username, password):
        self._username = username   # ENCAPSULATION
        self._password = password   # ENCAPSULATION

    def get_username(self):
        return self._username

    @abstractmethod
    def get_role(self):   # ABSTRACTION
        pass

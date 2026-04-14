from abc import ABC, abstractmethod            # Imported abstraction tools that will be used for this file.

class Person(ABC):                             # ABSTRACTION used, this abstracts the base class.

    def __init__(self, username, password):
        self._username = username              # ENCAPSULATION private sector, an attribute to be protected.
        self._password = password              # ENCAPSULATION private sector, an attribute to be protected.

    def get_username(self):                    # Getter method, wherein it gets the username as the new self.
        return self._username

    @abstractmethod
    def get_role(self):                        # ABSTRACTION used, which force subclasses to implement this method.
        pass

from models.person import Person

class Admin(Person):
    def __init__(self, username, password, admin_id):
        super().__init__(username, password)
        self.__admin_id = admin_id

    def verify_admin(self, admin_id):
        return self.__admin_id == admin_id

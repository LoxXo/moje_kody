from dataclasses import dataclass
from typing import Iterable
from unittest.mock import Mock, MagicMock


@dataclass
class User:
    id: int
    name: str


class Db:
    """
    Klasa dostępu do storeage'a userów... prawdopodobnie bazy na zewnętrznym serwerze.
    """

    def get_version(self):
        return "0.0.1"

    def all_users(self) -> Iterable[User]:
        """
        :return: Iterable of all users in the database.
        """
        raise NotImplemented()

    def add_user(self, u: User):
        if u in db.all_users():
            raise RuntimeError("ID is already in database")
        else:
            return db.all_users.append(u)


class AuthChecker:
    db: Db

    def __init__(self, db: Db):
        self.db = db

    def is_user(self, id: int):
        user_ids = [u.id for u in db.all_users()]
        return id in user_ids


if __name__ == "__main__":
    # tworzenie kontekstu
    db = Db()
    auth = AuthChecker(db)

    # mock-owanie i testowanie
    # print(db.get_version())
    # users = db.all_users()

    # db.all_users = MagicMock(
    #     return_value=[User(2, 'Xi'), User(5, 'Jair')])  # podmieniamy prawdziwą metodę, i piszemy co ma zwrócić

    # db.all_users.side_effect = [[User(2,'Xi')], []]   # todo: multiple values

    db.all_users = MagicMock(
        return_value=[]
    )  # podmieniamy prawdziwą metodę, i piszemy co ma zwrócić
    print(db.all_users())
    print(auth.is_user(2))

    db.all_users = MagicMock(return_value=[User(3, "Smith"), User(4, "Smith")])
    print(db.all_users())
    print(auth.is_user(3))

    db.add_user = MagicMock()
    # print(db.all_users.mock_calls)  # z tego można zobaczyć jakie zapytania do metody `all_users` zostały wykonane
    # db.all_users.assert_called()    # rzuci błędem, jeśli ta metoda nie została uruchomiona

    # users = db.all_users()
    # print(users)

    # a = AuthChecker(db)
    # print(a.is_user(2))
    # print(a.is_user(3))

from dataclasses import dataclass
from typing import Iterable
from unittest.mock import Mock, MagicMock


@dataclass
class User:
    id: int
    name: str

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name


class Db:
    """
    Klasa dostępu do storeage'a userów... prawdopodobnie bazy na zewnętrznym serwerze.
    """

    userdb: Iterable[User]

    def __init__(self, udb: Iterable[User]):
        self.userdb = udb

    def __repr__(self):
        return f"Pełna baza: {self.userdb}"

    def get_version(self):
        return "0.0.1"

    def all_users(self) -> Iterable[User]:
        """
        :return: Iterable of all users in the database.
        """
        return self.userdb

    def add_user(self, u: User):
        used_id = [u.id for u in self.userdb]
        if u.id in used_id:
            raise RuntimeError(f"Nr {u.id} ID is already in database")
        else:
            return self.userdb.append(u)

    def del_user(self, del_id: int):
        used_id = [
            u.id for u in self.userdb
        ]  ## mozna usunac po indexie tuple w list'cie
        if del_id in used_id:
            del self.userdb[used_id.index(del_id)]
        else:
            raise RuntimeError(f"Cannot delete, there is no user with nr {id} ID")


class AuthChecker:
    db: Db

    def __init__(self, db: Db):
        self.db = db

    def is_user(self, id: int):
        user_ids = [u.id for u in db.all_users()]
        return id in user_ids


if __name__ == "__main__":
    # tworzenie kontekstu
    db = Db([])
    auth = AuthChecker(db)

    # mock-owanie i testowanie
    # print(db.get_version())
    # users = db.all_users()

    # db.all_users = MagicMock(
    #     return_value=[User(2, 'Xi'), User(5, 'Jair')])  # podmieniamy prawdziwą metodę, i piszemy co ma zwrócić

    # db.all_users.side_effect = [[User(2,'Xi')], []]   # todo: multiple values

    # jak zrobić mock, a potem go cofnąć?
    """
    A - W klasie AuthChecker sprawdzić, czy metoda is_user funkcjonuje dobrze,
    jeśli w bazie nie ma żadnych userów
    """
    db.all_users = MagicMock(
        return_value=[]
    )  # podmieniamy prawdziwą metodę, i piszemy co ma zwrócić
    print(db.all_users())
    print(auth.is_user(2))
    """
    B - W klasie AuthChecker sprawdzić, czy metoda is_user działa dobrze,
    jeśli w bazie jest dwóch userów o tym samym name
    """
    db.all_users = MagicMock(return_value=[User(3, "Smith"), User(4, "Smith")])
    print(db.all_users())
    print(auth.is_user(3))
    """
    C - Do klasy Db dodać metodę add_user(u: User), która doda usera do bazy
    przy okazji sprawdzając,
    czy user o podanym id w bazie narazie nie istnieje
    """
    user1 = User(55, "Agent")
    user2 = User(111, "A.Smith")
    db.add_user(user1)
    db.add_user(user2)
    print(db)
    print(db.all_users())
    """
    D - Korzystając z wyniku (C) sprawdzić, czy AuthChecker działa poprawnie,
    czyli czy jeśli dodamy usera z id=111, to potem metoda is_user(111) zwróci True
    """
    print(auth.is_user(111))
    """
    E - Analogicznie dodać metodę remove_user(id:int) (do Db),
    która ma zapewnić, że usera o podanym id nie będzie już w bazie userów,
    oraz sprawdzić, czy natychmiast wynik ten jest widoczny w metodzie AuthChecker.is_user (jak powyżej)
    """
    db.del_user(55)
    print(db)

    # print(db.all_users.mock_calls)  # z tego można zobaczyć jakie zapytania do metody `all_users` zostały wykonane
    # db.all_users.assert_called()    # rzuci błędem, jeśli ta metoda nie została uruchomiona

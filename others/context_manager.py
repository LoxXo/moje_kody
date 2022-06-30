from abc import ABC


class BaseContextManager(ABC):
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        pass


class Otwieracz(BaseContextManager):
    def __init__(self, filename=None):
        self.filename = filename

    def __enter__(self):
        self.otwarty = open(self.filename)
        return self.otwarty

    def __exit__(self, exc_type, exc_value, traceback):
        breakpoint()
        self.otwarty.close()


if __name__ == "__main__":
    with Otwieracz("plik1") as otw:
        otw.close()
        print(otw.read())
        raise RuntimeError("dupa")

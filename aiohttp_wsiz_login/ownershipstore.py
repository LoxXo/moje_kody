import asyncio
import csv
from asyncio import sleep
from dataclasses import dataclass
from fileinput import filename
from typing import Dict
import logging


@dataclass
class FileMeta:
    filename: str
    studentid: int
    groupid: int


LOG = logging.getLogger()


class OwnershipStore:
    owners: Dict[str, FileMeta]  # filename -> FileMeta; prywatna

    def __init__(self):  # dane wczytane z pliku 'owners.csv'
        self.owners = dict()
        with open("owners.csv") as f:
            reader = csv.reader(f)
            for filename, studentid, groupid in reader:
                self.owners[filename] = FileMeta(filename, studentid, groupid)

    async def periodic_save(
        self,
    ):  #  co parę sekund zapisujemy dane tego serwisu do 'owners.csv'
        LOG.info("writing to owners.csv")
        while True:
            with open("owners.csv", "w", newline="") as w:
                ownerswriter = csv.writer(
                    w, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL
                )
                for filemeta in self.owners.values():
                    ownerswriter.writerow(
                        [filemeta.filename, filemeta.studentid, filemeta.groupid]
                    )
            await sleep(1)

    async def save_file(self, filemeta: FileMeta):  # tylko zapisać do self.owners
        self.owners[filemeta.filename] = filemeta
        await sleep(0.5)

    async def get_meta(
        self, filename: str
    ) -> FileMeta:  # tylko dane bezpośrednio z self.owners
        return self.owners[filename]

    async def can_read(self, filename: str, studentid: int):
        try:
            filemeta: FileMeta = self.owners[filename]
            if filemeta.groupid == "0" or filemeta.studentid == str(studentid):
                return True
            else:
                return False
        except:
            return False
        # logika sprawdzenia czy możemy czytać dany plik
        # ma sprawdzić FileMeta tego pliku..
        # i narazie: jeśli groupid==0 --> True, jeśli studentid==studentid --> True
        # else: False


async def main():
    store1 = OwnershipStore()
    print(store1.owners)
    asyncio.create_task(store1.periodic_save())
    await sleep(2)


if __name__ == "__main__":
    asyncio.run(main())

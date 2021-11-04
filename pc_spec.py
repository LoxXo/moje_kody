"""
Obiektowe klasy opisujące komputery PC (wolnostojące i laptopy)

- wykorzystać strukturę dziedziczenia 
- elemety typowe: 
   1. motherboard(1), 
   2. cpu(1),  
   3. memory_chip (DDR4, SODIMM, buffered-RAM) ... bank1..4,
   4. hard_drive (sata1..4), 
   5. pcie (3), 
   6. GPU (1)
  
- ustawić konstruktory tak by całość dało się spiąć poprawnie
- napisać kilka metod do operowania komputerem, i ukryć jego 
  zmienne (prywatne) tak by nie można było całośći "rozwalić"
  

User stories: 
- mamy PC, przy konstrukcji musimy podać MB, oraz CPU, List[RAM], GPU na PCIe
  ↑↑ to w konstuktorze
  
- PC powinien mieć własność running/not-running
- przy wyłączonym można wymianiać wszystko.... ale metodami, nie przez zmianę zmiennych
- metody powinny brać pozycję na którą instalujemy sprzęt
- powinny być dostępne gettery by sprawdzić co gdzie jest zamontowane

dodac TDP dla sprzetu i zrobic zliczanie łącznego zużycia ()
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class Power:  ## unused
    power_TDP: int


class Component:
    __is_connected: bool = False

    def __init__(self, connected: bool):
        self.__is_connected = connected

    def connect(self):
        if self.__is_connected == True:
            raise RuntimeError("Component is already connected")
        self.__is_connected = True
        return print(f"{type(self).__name__} is connected")

    def disconnect(self):
        if self.__is_connected == False:
            raise RuntimeError("Component is disconnected")
        self.__is_connected = False
        return print(f"{type(self).__name__} is disconnected")

    @property
    def is_connected(self) -> bool:
        return self.__is_connected


class CPU_List(Enum):  # simplifed mobo compability
    i9_11900 = "LGA1200"
    i7_11700 = "LGA1200"
    i5_8600 = "LGA1151"
    r5_5600X = "AM4"


class CPU(Component, Power):
    __model: str
    __gen_socket: str
    __cores: int
    __clock_GHz: float

    def __init__(self, model: str, cores: int, clock: float):
        self.__model = model
        self.__cores = cores
        self.__clock_GHz = clock

    def __repr__(self):
        return f"{self.__model}, {self.__gen_socket}, {self.__cores} cores, {self.__clock_GHz} MHz"

    # getter
    @property
    def model(self) -> str:
        return self.__model

    @property
    def cores(self) -> int:
        return self.__cores

    @property
    def clock_GHz(self) -> float:
        return self.__clock_GHz

    @property
    def gen_socket(self) -> str:
        return self.__gen_socket

    @property
    def is_connected(self) -> bool:
        return self.__is_connected

    def set_socket(self):
        self.__gen_socket = CPU_List[self.__model].value


class Memory(Component, Power):
    __sizeGB: int
    __stock_frequency: int
    __max_frequency: int  # according to max mobo freq

    def __init__(self, sizeGB: int, stock_freq: int):
        self.__sizeGB = sizeGB
        self.__stock_frequency = stock_freq

    def __repr__(self):
        return f"{self.__sizeGB} GB, {self.__stock_frequency} stock MHz, {self.__max_frequency} max MHz"

    @property
    def mem_size(self):
        return self.__sizeGB

    @property
    def frequency(self):
        return self.__max_frequency

    @property
    def is_connected(self) -> bool:
        return self.__is_connected

    @frequency.setter
    def frequency(self, mobo_freq: int):
        self.__max_frequency = min(self.__stock_frequency, mobo_freq)


class Hard_drive(Component, Power):
    __sizeinGB = int
    __read_speed = float
    __write_speed = float

    def __init__(self, size: int, read: float, write: float):
        self.__sizeinGB = size
        self.__read_speed = read
        self.__write_speed = write

    def __repr__(self):
        return f"{self.__sizeinGB} GB, read speed: {self.__read_speed}, write speed: {self.__write_speed}"

    @property
    def is_connected(self) -> bool:
        return self.__is_connected


class GPU(Component):
    __brand: str
    __model: str
    __clock: float
    __memoryinGB: float

    def __init__(self, brand: str, model: str, clock: float, memory: float):
        self.__brand = brand
        self.__model = model
        self.__clock = clock
        self.__memoryinGB = memory

    def __repr__(self) -> str:
        return f"{self.__brand}, {self.__model}, {self.__clock} MHz, {self.__memoryinGB} GB"

    @property
    def brand(self) -> str:
        return self.__brand

    @property
    def model(self) -> str:
        return self.__model

    @property
    def clock(self) -> float:
        return self.__clock

    @property
    def memory(self) -> float:
        return self.__memoryinGB


@dataclass
class Motherboard(Component, Power):
    __brand: str
    __cpu_socket: str
    __ram_slots: List[Optional[Memory]]
    __ram_max_frequency: int
    __sata_slots: List[Optional[Hard_drive]]
    __cpu: str = None
    __gpu: str = None

    def __init__(
        self,
        brand: str,
        cpu_socket: str,
        ram_slots: int,
        ram_max_freqeuncy: int,
        sata_slots: int,
    ):
        self.__brand = brand
        self.__cpu_socket = cpu_socket
        self.__ram_slots = [None] * ram_slots
        self.__ram_max_frequency = ram_max_freqeuncy
        self.__sata_slots = [None] * sata_slots

    def __repr__(self) -> str:
        return (
            f"Mobo brand: {self.__brand};\nSocket: {self.__cpu_socket}, CPU: {self.__cpu};\n"
            f"Ram slots: {self.__ram_slots}; Mobo ram max freq: {self.__ram_max_frequency};\n"
            f"HDD:{self.__sata_slots};\nGPU: {self.__gpu}"
        )

    def insert_cpu(self, new_cpu: CPU):
        if self.__cpu_socket is not new_cpu.gen_socket:
            raise RuntimeError("Wrong CPU socket")
        self.__cpu = new_cpu
        new_cpu.connect()

    def insert_ram(self, new_ram: Memory, slot: int):
        if len(self.__ram_slots) < slot:
            raise RuntimeError(
                "Nie mozesz wsadzic do tego slota, on nie istnieje i nie moze cie skrzywdzic"
            )
        if self.__ram_slots[slot] is not None:
            raise RuntimeError(f"Slot {slot} is occupied")
        new_ram.frequency = self.__ram_max_frequency
        self.__ram_slots[slot] = new_ram
        new_ram.connect()

    def insert_hdd(self, new_hdd: Hard_drive, slot: int):
        if len(self.__sata_slots) < slot:
            raise RuntimeError(f"Sata slot number {slot} is not existing")
        if self.__sata_slots[slot] is not None:
            raise RuntimeError(f"Slot {slot} is occupied")
        self.__sata_slots[slot] = new_hdd
        new_hdd.connect()

    def insert_gpu(self, new_gpu: GPU):
        self.__gpu = new_gpu
        new_gpu.connect()

    def remove_cpu(self):
        if self.__cpu is not None:
            cpu = self.cpu
            self.__cpu = None
            cpu.disconnect()
        else:
            raise RuntimeError("CPU slot is already empty")

    def remove_ram(self, slot: int):
        if self.__ram_slots[slot] is not None:
            ram = self.__ram_slots[slot]
            self.__ram_slots[slot] = None
            ram.disconnect()
        else:
            raise RuntimeError(f"RAM slot nr {slot} is already empty")

    def remove_hdd(self, slot: int):
        if self.__sata_slots[slot] is not None:
            hdd = self.__sata_slots[slot]
            self.__sata_slots[slot] = None
            hdd.disconnect()
        else:
            raise RuntimeError(f"Sata slot {slot} is already empty")

    def remove_gpu(self):
        if self.__gpu is not None:
            gpu = self.__gpu
            self.__gpu = None
            gpu.disconnect()
        else:
            raise RuntimeError("GPU slot is already empty")

    @property
    def memory_size(self):
        return sum([mem.mem_size for mem in self.__ram_slots if mem is not None])

    @property
    def cpu(self) -> str:
        return self.__cpu

    @property
    def ram_slots(self):
        return self.__ram_slots


class PC:
    __running = False
    __motherboard: Motherboard

    def __init__(self, pcmobo: Motherboard):
        self.__motherboard = pcmobo

    def __repr__(self) -> str:
        mobo_repr = self.__motherboard.__repr__()
        return f"PC info:\n{mobo_repr}"

    def run_PC(self):
        if (
            self.__motherboard.cpu is not None
            and any(self.__motherboard.ram_slots) is True
        ):
            self.__running = True
            print("PC is running")
        else:
            raise RuntimeError("Some necessary components aren't connected")

    def shutdown_pc(self):
        self.__running = False
        print("PC was shut down")


if __name__ == "__main__":
    ram1 = Memory(8, 2666)
    ram2 = Memory(8, 3400)
    cpu1 = CPU("i9_11900", 8, 3600)
    gpu1 = GPU("Radeon", "RX 6900 XT", 2285, 16)
    mobo = Motherboard("ABC", "LGA1200", 4, 3200, 6)
    hdd1 = Hard_drive(1000, 200, 160)

    cpu1.set_socket()
    mobo.insert_ram(ram1, 0)
    mobo.insert_ram(ram2, 2)
    mobo.insert_cpu(cpu1)
    mobo.insert_hdd(hdd1, 0)
    mobo.insert_gpu(gpu1)
    pc1 = PC(mobo)
    pc1.run_PC()
    print(pc1)

    mobo.remove_cpu()
    mobo.remove_ram(2)
    print(pc1)

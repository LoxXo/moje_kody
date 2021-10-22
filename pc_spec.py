### Obiektowe klasy opisujące komputery PC (wolnostojące i laptopy)

# - wykorzystać strukturę dziedziczenia 
# - elemety typowe: 
#    1. motherboard(1), 
#    2. cpu(1),  
#    3. memory_chip (DDR4, SODIMM, buffered-RAM) ... bank1..4,
#    4. hard_drive (sata1..4), 
#    5. pcie (3), 
#    6. GPU (1)
  
# - ustawić konstruktory tak by całość dało się spiąć poprawnie
# - napisać kilka metod do operowania komputerem, i ukryć jego 
#   zmienne (prywatne) tak by nie można było całośći "rozwalić"
  

# User stories: 
# - mamy PC, przy konstrukcji musimy podać MB, oraz CPU, List[RAM], GPU na PCIe
#   ↑↑ to w konstuktorze
  
# - PC powinien mieć własność running/not-running
# - przy wyłączonym można wymianiać wszystko.... ale metodami, nie przez zmianę zmiennych
# - metody powinny brać pozycję na którą instalujemy sprzęt
# - powinny być dostępne gettery by sprawdzić co gdzie jest zamontowane

# dodac TDP dla sprzetu i zrobic zliczanie łącznego zużycia ()
# enum 

class Power:
    power_TDP: int

class Component:
    is_connected: bool = False

    def connect (self):
        if self.is_connected == True:
            raise Exception("Component is already connected")
        self.is_connected = True
        return self

    def disconnect (self):
        if self.is_connected == False:
            raise Exception("Component is disconnected")
        self.is_connected = False
        return self

class Motherboard:
    __brand: str
    __cpu_socket: str
    __ram_slots = int
    __ram_max_frequency = int


class Intel_Motherboard(Motherboard):
    pass

class AMD_Motherboard(Motherboard):
    pass

class CPU:
    __clock: float
    __gen_socket: str

class Intel_CPU(CPU):
    
    pass

class AMD_CPU(CPU):
    
    pass

class Memory:
    bank_nr: int[1,2,3,4]


class Hard_drive:
    sizeingb = float


class Pcie:
    pass

class GPU:
    clock: float
    memoryinGB: float


class PC(Motherboard, CPU, Memory, Hard_drive, Pcie, GPU):
    running = False

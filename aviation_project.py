from dataclasses import dataclass
from typing import List
from math import cos, asin, sqrt, pi


@dataclass
class Location:
    lat: float
    lon: float

    def distance_calc(
        self, destination: "Location"
    ) -> (float):  # Haversine formula in km
        lat1 = self.lat
        lat2 = destination.lat
        lon1 = self.lon
        lon2 = destination.lon
        p = pi / 180
        a = (
            0.5
            - cos((lat2 - lat1) * p) / 2
            + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
        )
        return 12742 * asin(sqrt(a))  # 2*Earth_R*asin...


class Passenger:
    location: Location
    healthy = True

    def health_check(list_passenger):
        for passenger in list_passenger:
            if passenger.healthy == False:
                return print(
                    "Some passengers are not healthy. Abording taxiing procedure."
                )
        return print("All passengers are healthy. Airplane is ready to go.")

    def __init__(
        self, location, healthy
    ):  # constructor to test difference when using print
        self.location = location
        self.healthy = healthy

    def __repr__(self):
        return f"{self.location} {self.healthy}"


@dataclass
class Pilot:
    name: str
    location: Location
    healthy = True


@dataclass
class Airplane:
    pilot1: "Pilot"
    passengers: List["Passenger"]
    location: Location
    type: int
    fuel_tank: float
    fuel_consumption: float
    healthy = True

    def fly(self, destination):
        self.fuel_tank = (
            self.fuel_tank
            - self.location.distance_calc(destination) * self.fuel_consumption
        )
        self.location = destination
        self.pilot1.location = destination
        for passenger in self.passengers:
            passenger.location = destination


airports = {"KTW": Location(50.474167, 19.08), "WAW": Location(52.165833, 20.967222)}


if __name__ == "__main__":
    p1 = Passenger(airports["KTW"], True)
    p2 = Passenger(airports["KTW"], False)
    # p3 = Passenger(airports["WAW"], True)

    pilot1 = Pilot("John Smith", airports["KTW"])
    # pilot2 = Pilot("William Hoover", airports["WAW"])

    airplane1 = Airplane(pilot1, [p1, p2], airports["KTW"], 1, 500, 10)
    # airplane2 = Airplane(pilot2, [p3], airports["WAW"], 2, 500, 15)

    destination = airports["WAW"]

    flight_distance = Location.distance_calc(airplane1.location, destination)

    print(f"Pilot {airplane1.pilot1.name} is assigned for this flight.\n")
    print(f"Distance between airports totals {flight_distance} kilometers\n")
    print(
        f"Starting Ground Operations. {len(airplane1.passengers)} passengers boarded the plane.\n"
    )
    Passenger.health_check(airplane1.passengers)
    airplane1.fly(destination)

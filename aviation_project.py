from typing import List
from math import cos, asin, sqrt, pi

class Pilot:
    healthy = True


class Passenger:
    healthy = True

class Location:
    KTW = Location(50.474167, 19.08)
    

    def distance(lat1, lon1, lat2, lon2):
        p = pi/180
        a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
        return 12742 * asin(sqrt(a)) #2*R*asin...

class Airplane:
    pilot1: 'Pilot'
    passengers: List['Passenger']
    type: int
    fuel: float
    healthy = True
    

__author__ = 'boyang'
import math


def distance(longitude_1: float, latitude_1: float, longitude_2: float, latitude_2: float) -> float:
    #guoyongran
    #get the distance of two point,every point have two values(longitude（经度）,latitude（纬度）).
    """
    belong:
        barber/barbers.py
    para:
        float
    return:
        float(meters)
    """

    rad_lat_1, rad_lat_2 = latitude_1*math.pi/180.0, latitude_2*math.pi/180.0

    a = rad_lat_1 - rad_lat_2
    b = longitude_1*math.pi/180.0 - longitude_2*math.pi/180.0

    s = 2 * math.asin(math.sqrt(math.pow(math.sin(a / 2), 2) +
                                math.cos(rad_lat_1) *
                                math.cos(rad_lat_2) *
                                math.pow(math.sin(b/2), 2)))
    earth_radius = 6378.137
    return abs(int(s * earth_radius * 1000))

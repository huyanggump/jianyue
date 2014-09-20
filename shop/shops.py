__author__ = 'boyang'

from shop.models import Shop
from robust.checker import Checker
from robust.exception import *
from utilities.numeric import distance


class ShopsManager:
    @classmethod
    def get_near_shop(cls, *, longitude, latitude, range_):
        shops = Shop.objects.all()
        in_range = lambda shop: distance(longitude_1=longitude,
                                         latitude_1=latitude,
                                         longitude_2=shop.shop_long,
                                         latitude_2=shop.shop_lati) < range_
        return [ShopProxy.get_by_object(shop).get_dict() for shop in shops if in_range(shop)]


class ShopProxy:
    def __init__(self, name):  # name is not a unique key.
        try:
            self.__shop = Shop.objects.get(shop_name=name)
        except Shop.DoesNotExist:
            raise ShopDoesNotExistError

    @classmethod
    def get_by_object(cls, shop):
        s = cls.__new__(cls)
        s.__shop = shop
        return s

    @property
    def name(self):
        return self.__shop.shop_name

    @name.setter
    def name(self, name_):
        Checker.name(name_)
        self.__shop.shop_name = name_
        self.__shop.save()

    @property
    def address(self):
        return self.__shop.shop_add

    @address.setter
    def address(self, address_):
        Checker.address(address_)
        self.__shop.shop_add = address_
        self.__shop.save()

    @property
    def longitude(self):
        return self.__shop.shop_long

    @longitude.setter
    def longitude(self, longitude_):
        Checker.longitude(longitude_)
        self.__shop.shop_long = longitude_
        self.__shop.save()

    @property
    def latitude(self):
        return self.__shop.shop_lati

    @latitude.setter
    def latitude(self, latitude_):
        Checker.latitude(latitude_)
        self.__shop.shop_lati = latitude_
        self.__shop.save()

    @property
    def phone(self):
        return self.__shop.shop_phone

    @phone.setter
    def phone(self, phone_):
        Checker.phone(phone_)
        self.__shop.shop_phone = phone_
        self.__shop.save()

    def get_dict(self):
        return {'shop': self.__shop.shop_name, 'address': self.__shop.shop_add}





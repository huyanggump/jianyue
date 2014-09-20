__author__ = 'boyang'
from utilities.numeric import distance
from barber.models import Barber, Hairstyle
from shop.models import Shop
from robust.checker import Checker
from robust.exception import *
#The BarbersManager class can manage barbers' information, such as add ,update, delete, query
#proxy layer


class BarbersManager:
    #负责管理整个barber表， 相当于是QuerySet的一个代理
    @classmethod
    def get_near_barber(cls, *, longitude, latitude, range_):
        Checker.latitude(latitude).longitude(longitude)
        barbers = Barber.objects.all()
        d = lambda barber_: distance(latitude_1=latitude, longitude_1=longitude,
                                     latitude_2=barber_.barber_shop_id.shop_lati,
                                     longitude_2=barber_.barber_shop_id.shop_long)
        barbers_in_range, dis_list = [], []
        for barber in barbers:
            temp = d(barber)
            if temp < range_:
                barbers_in_range.append(BarberProxy.get_by_object(barber))
                dis_list.append(temp)
        return barbers_in_range, dis_list

    @classmethod
    def add_barber(cls, *, phone, password, name, sex, shop, time_):
        try:
            barber = Barber()
            Checker.phone(phone).password(password).name(name).sex(sex).shop_name(shop).time_set(time_)
            para = (phone, password, name, sex, Shop.objects.get(shop_name=shop), time_)

            (barber.barber_phone, barber.barber_pass, barber.barber_name,
             barber.barber_sex, barber.barber_shop_id, barber.free_time) = para

            barber.save()
        except Shop.DoesNotExist:
            raise ShopDoesNotExistError

    @classmethod
    def get_all_barber(cls):
        barbers = Barber.objects.all()
        return [BarberProxy.get_by_object(barber) for barber in barbers]


class BarberProxy:
    #负责处理单个barber对象

    def __init__(self, phone):
        try:
            self.__barber = Barber.objects.get(barber_phone=phone)
        except Barber.DoesNotExist:
            raise BarberDoesNotExistError

    @classmethod
    def get_by_object(cls, barber):
        b = cls.__new__(cls)
        b.__barber = barber
        return b

    @property
    def shop(self):
        return self.__barber.barber_shop_id.shop_name

    @shop.setter
    def shop(self, shop_name):
        try:
            self.__barber.barber_shop_id = Shop.objects.get(shop_name=shop_name)
            self.__barber.save()
        except Shop.DoesNotExist:
            raise ShopDoesNotExistError

    @property
    def address(self):
        return self.__barber.barber_shop_id.shop_add

    @property
    def name(self):
        return self.__barber.barber_name

    @name.setter
    def name(self, name_):
        Checker.name(name_)
        self.__barber.barber_name = name_
        self.__barber.save()

    @property
    def longitude(self):
        return self.__barber.barber_shop_id.shop_long

    @property
    def latitude(self):
        return self.__barber.barber_shop_id.shop_lati

    @property
    def sex(self):
        return self.__barber.barber_sex

    @sex.setter
    def sex(self, sex_):
        Checker.sex(sex_)
        self.__barber.barber_sex = sex_
        self.__barber.save()

    @property
    def phone(self):
        return self.__barber.barber_phone

    @phone.setter
    def phone(self, phone_):
        Checker.phone(phone_)
        self.__barber.barber_phone = phone_
        self.__barber.save()

    @property
    def time(self):
        return self.__barber.free_time

    @time.setter
    def time(self, time_):
        Checker.time_set(time_)
        self.__barber.free_time = time_
        self.__barber.save()

    def match(self, password: str) -> bool:
        if not self.__barber.barber_pass == password:
            raise PasswordDoesNotMatch

    def set_appt_time(self, time_):
        #理发师设置自己的可预约时间
        Checker.time_set(time_)  # 检查设置的预约时间是否合法
        self.__barber.free_time = time_
        self.__barber.save()

    def get_dict(self):
        return {'phone': self.__barber.barber_phone,
                'name': self.__barber.barber_name,
                'sex': self.__barber.barber_sex,
                'longitude': self.__barber.barber_shop_id.shop_long,
                'latitude': self.__barber.barber_shop_id.shop_lati,
                'shop': self.__barber.barber_shop_id.shop_name,
                'address': self.__barber.barber_shop_id.shop_add}


class HairstyleProxy:  # 有问题的部分
    def __init__(self, name_):
        try:
            self.__hairstyle = Hairstyle.objects.get(hairstyle_name=name_)
        except Hairstyle.DoesNotExist:
            raise HairstyleDoesNotExistError

    @property
    def name(self):
        return self.__hairstyle.hairstyle_name

    @property
    def time(self):
        return self.__hairstyle.hairstyle_time
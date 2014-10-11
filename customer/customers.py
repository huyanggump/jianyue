__author__ = 'boyang'

from customer.models import Customer
from robust.exception import *
from robust.checker import Checker


class CustomersManager:
    @classmethod
    def add_customer(cls, *, phone: str, name: str, sex: str):  # 如何防止重复
        try:
            _ = CustomerProxy(phone)
        except CustomerDoesNotExistError:
            Checker.phone(phone).name(name).sex(sex)
            customer = Customer()
            customer.cus_name, customer.cus_phone, customer.cus_sex = name, phone, sex
            customer.save()


class CustomerProxy:
    def __init__(self, phone):
        try:
            self.__customer = Customer.objects.get(cus_phone=phone)
        except Customer.DoesNotExist:
            raise CustomerDoesNotExistError

    @classmethod
    def get_by_object(cls, customer: Customer):
        c = cls.__new__(cls)
        c.__customer = customer
        return c

    @property
    def name(self):
        return self.__customer.cus_name

    @name.setter
    def name(self, name_):
        Checker.name(name_)
        self.__customer.cus_name = name_
        self.__customer.save()

    @property
    def phone(self):
        return self.__customer.cus_phone

    @phone.setter
    def phone(self, phone_):
        Checker.phone(phone_)
        self.__customer.cus_phone = phone_
        self.__customer.save()

    @property
    def sex(self):
        return self.__customer.cus_sex

    @sex.setter
    def sex(self, sex_):
        Checker.sex(sex_)
        self.__customer.cus_sex = sex_
        self.__customer.save()

    @property
    def profile(self):
        return self.__customer.cus_profile

    @profile.setter
    def profile(self, image):
        Checker.profile(image)
        self.__customer.cus_profile = image
        self.__customer.save()

    def get_dict(self):
        return {'name': self.__customer.cus_name,
                'phone': self.__customer.cus_phone,
                'sex': self.__customer.cus_sex}
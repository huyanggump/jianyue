__author__ = 'boyang'
from order.models import Order
from barber.barbers import Barber
from barber.models import Hairstyle
from robust.checker import Checker
from robust.exception import *
from customer.models import Customer


class OrdersManager:

    @classmethod
    def add_order(cls, *, cus_phone, bar_phone=None, time_=None, accepted=None, hairstyle=None, remark=None):
        try:
            Checker.phone(cus_phone)
            order = Order()
            order.ord_cus_id = Customer.objects.get(cus_phone=cus_phone)
            if bar_phone:
                Checker.phone(bar_phone)
                order.ord_barber_id = Barber.objects.get(barber_phone=bar_phone)
            if time_:
                Checker.appt_time(time_)  #
                order.ord_time = time_
            if accepted is not None:
                order.ord_is_acc = accepted
            if hairstyle:
                order.ord_hairstyle_id = Hairstyle.objects.get(hairstyle_name=hairstyle)
            if remark:
                order.ord_remark = remark
            order.save()
            return OrderProxy.get_by_object(order)
        except Customer.DoesNotExist:
            raise CustomerDoesNotExistError
        except Barber.DoesNotExist:
            raise BarberDoesNotExistError
        except Hairstyle.DoesNotExist:
            raise HairstyleDoesNotExistError

    @classmethod
    def get_by_time(cls, *, start, end):
        orders = Order.objects.all()
        test = lambda time_: time_ and len(time_) >= 22 and start < time_ < end  # 订单中有时间字段有可能有空串
        return [OrderProxy.get_by_object(order) for order in orders if test(order.ord_time)]

    @classmethod
    def get_by_cus(cls, phone):
        orders = Order.objects.all()
        t = lambda order: Customer.objects.get(cus_phone=phone).cus_id == order.ord_cus_id###proxy不做谁来做？
        return [OrderProxy.get_by_object(order) for order in orders if t(order)]


class OrderProxy:

    def __init__(self, order_id):
        try:
            self.__order = Order.objects.get(ord_id=order_id)
        except Order.DoesNotExist:
            raise OrderDoesNotExistError

    @classmethod
    def get_by_object(cls, order):
        o = cls.__new__(cls)
        o.__order = order
        return o

    @property
    def cus_name(self):
        return self.__order.ord_cus_id.cus_name

    @property
    def cus_phone(self):
        return self.__order.ord_cus_id.cus_phone

    @property
    def bar_phone(self):
        return self.__order.ord_barber_id.barber_phone

    @bar_phone.setter
    def bar_phone(self, phone):
        Checker.phone(phone)
        try:
            self.__order.ord_barber_id = Barber.objects.get(bar_phone=phone)
            self.__order.save()
        except Barber.DoesNotExist:
            raise BarberDoesNotExistError

    @property
    def bar_name(self):
        return self.__order.ord_barber_id.barber_name

    @property
    def time(self):
        return self.__order.ord_time

    @time.setter
    def time(self, time_):
        Checker.appt_time(time_)
        self.__order.ord_time = time_
        self.__order.save()

    @property
    def accepted(self):
        return self.__order.ord_is_acc

    @accepted.setter
    def accepted(self, accepted_):
        self.__order.ord_is_acc = accepted_
        self.__order.save()

    @property
    def hairstyle(self):
        return self.__order.ord_hairstyle_id.hairstyle_name

    @hairstyle.setter
    def hairstyle(self, hairstyle_):
        try:
            self.__order.ord_hairstyle_id = Hairstyle.objects.get(hairstyle_name=hairstyle_)
            self.__order.save()
        except Hairstyle.DoesNotExist:
            raise HairstyleDoesNotExistError

    @property
    def remark(self):
        return self.__order.ord_remark

    @remark.setter
    def remark(self, remark_):
        Checker.remark(remark_)
        self.__order.ord_remark = remark_
        self.__order.save()

    def update(self, bar_phone, time_, accepted, hairstyle=None, remark=None):
        try:
            Checker.phone(bar_phone).appt_time(time_)  # ??
            self.__order.ord_barber_id = Barber.objects.get(barber_phone=bar_phone)
            self.__order.ord_time = time_
            self.__order.ord_is_acc = accepted
            if remark:
                Checker.remark(remark)
                self.__order.ord_remark = remark
            if hairstyle:
                self.__order.ord_hairstyle_id = Hairstyle.objects.get(hairstyle_name=hairstyle)
            self.__order.save()
            return self
        except Barber.DoesNotExist:
            raise BarberDoesNotExistError
        except Hairstyle.DoesNotExist:
            raise HairstyleDoesNotExistError

    def get_dict(self):
        result = {'cusphone': self.__order.ord_cus_id.cus_phone,
                  'cusname': self.__order.ord_cus_id.cus_name,
                  'barphone': None, 'barname': None, 'hairstyle': None,
                  'accepted': self.__order.ord_is_acc, 'remark': None, 'time': None}
        if self.__order.ord_barber_id:
            result['barname'] = self.__order.ord_barber_id.barber_name
            result['barphone'] = self.__order.ord_barber_id.barber_phone
        if self.__order.ord_hairstyle_id:
            result['hairstyle'] = self.__order.ord_hairstyle_id.hairstyle_name
        if self.__order.ord_remark:
            result['remark'] = self.__order.ord_remark
        if self.__order.ord_time:
            result['time'] = self.__order.ord_time
        return result

__author__ = 'boyang'
from abc import ABCMeta, abstractmethod


class JianyueError(Exception, metaclass=ABCMeta):
    @property
    @abstractmethod
    def info(self):
        return {'code': 0, 'log': 'Jianyue Error'}


class ServerInternalError(JianyueError):

    @property
    def info(self):
        return {'code': 200, 'log': 'Server Internal Error'}


class RequestError(JianyueError):
    @property
    def info(self):
        return {'code': 300, 'log': 'request error'}


class PassValueError(JianyueError):
    @property
    def info(self):
        return {'code': 400, 'log': 'pass value error'}


class NoException(JianyueError):
    @property
    def info(self):
        return {'code': 500, 'log': 'request error'}


class RequestKeyError(RequestError):
    @property
    def info(self):
        return {'code': 101, 'log': 'request key error'}


class RequestMethodError(RequestError):
    @property
    def info(self):
        return {'code': 102, 'log': 'request method error'}


class SexError(PassValueError):
    @property
    def info(self):
        return {'code': 401, 'log': 'Sex info should be "Male" or "Female"'}


class UserNameError(PassValueError):
    @property
    def info(self):
        return {'code': 402, 'log': 'Name should shorter than 4 characters length'}


class LongitudeError(PassValueError):
    @property
    def info(self):
        return {'code': 403, 'log': 'longitude are in range of (-180, 180)'}


class LatitudeError(PassValueError):
    @property
    def info(self):
        return {'code': 404, 'log': 'longitude are in range of (-90, 90)'}


class PhoneError(PassValueError):
    @property
    def info(self):
        return {'code': 405, 'log': 'Phone number is illegal'}


class RemarkError(PassValueError):
    @property
    def info(self):
        return {'code': 406, 'log': 'Remark should less than 26 words'}


class AddressError(PassValueError):
    @property
    def info(self):
        return {'code': 407, 'log': 'Remark should less than 26 words'}


class AppointmentDateError(PassValueError):
    @property
    def info(self):
        return {'code': 408, 'log': 'Date error'}


class TimeSetError(PassValueError):
    @property
    def info(self):
        return {'code': 409, 'log': 'Time set error'}


class DistanceError(PassValueError):

    @property
    def info(self):
        return {'code': 410, 'log': 'Distance error'}


class AppointmentTimeError(PassValueError):
    @property
    def info(self):
        return {'code': 411, 'log': 'Appointment Time Error'}


class PasswordError(PassValueError):
    @property
    def info(self):
        return {'code': 412, 'log': 'Password are too weak'}


class DataBaseError(ServerInternalError):
    @property
    def info(self):
        return {'code': 201, 'log': 'Database error'}


class BarberDoesNotExistError(DataBaseError):
    @property
    def info(self):
        return {'code': 202, 'log': 'No barber'}


class CustomerDoesNotExistError(DataBaseError):
    @property
    def info(self):
        return {'code': 203, 'log': 'No customer'}


class ShopDoesNotExistError(DataBaseError):
    @property
    def info(self):
        return {'code': 204, 'log': 'No shop'}


class HairstyleDoesNotExistError(DataBaseError):
    @property
    def info(self):
        return {'code': 205, 'log': 'No hairstyle'}


class PushError(ServerInternalError):
    @property
    def info(self):
        return {'code': 207, 'log': 'Push Error'}


class OrderDoesNotExistError(DataBaseError):
    @property
    def info(self):
        return {'code': 206, 'log': 'Order does not exist'}


class OrderTimeClash(NoException):
    @property
    def info(self):
        return {'code': 501, 'log': 'order time clash'}


class OrderHasAccepted(NoException):
    @property
    def info(self):
        return {'code': 505, 'log': 'order has accepted'}


class NoBarberHasRegister(NoException):
    @property
    def info(self):
        return {'code': 502, 'log': 'no barber nearby'}


class PasswordDoesNotMatch(NoException):
    @property
    def info(self):
        return {'code': 503, 'log': 'password does not match'}


class BarberHasRegister(NoException):
    @property
    def info(self):
        return {'code': 504, 'log': 'Barber has register'}




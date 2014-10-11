__author__ = 'boyang'
import re
import time
from robust.exception import *


class Checker:
    @classmethod
    def longitude(cls, longitude):
        if type(longitude) == float:
            if -180 < longitude < 180:
                return cls
            else:
                raise LongitudeError
        else:
            raise LongitudeError

    @classmethod
    def latitude(cls, latitude):
        if type(latitude) == float:
            if -90 < latitude < 90:
                return cls
            else:
                raise LatitudeError
        else:
            raise LatitudeError

    @classmethod
    def sex(cls, sex):
        if sex in {'Male', 'Female'}:
            return cls
        else:
            raise SexError

    @classmethod
    def appt_date(cls, date):
        """(str)->(boolean)

        >>> check_date('2014.04.06')
        False
        >>> check_date('2014.4.6')
        False
        >>> check_date('2014.09.01')
        True
        >>> check_date('2014.10.01')
        False
        >>> check_date('2014.06.01')
        False
        >>> check_date('2014.08.31')
        True
        """
        def leap(year):
            if year % 4 == 0:
                if year % 400 == 0:
                    return 29
                else:
                    if year % 100 == 0:
                        return 28
                    else:
                        return 29
            else:
                return 28
        format_time = time.strftime('%Y.%m.%d', time.localtime(time.time()))
        max_day = {'01': 31, '02': leap(int(format_time[0:4])), '03': 31,'04': 30,
                   '05': 31, '06': 30, '07': 31, '08': 31,
                   '09': 30, '10': 31, '11': 30, '12': 31}
        pattern = re.compile(r"[0-9][0-9][0-9][0-9].[0-9][0-9].[0-9][0-9]")
        if pattern.match(date):
            if format_time[0:5] == date[0:5]:
                month_plus_one = format_time[5:7]
                month_plus_one = str(int(month_plus_one) + 1)
                if len(month_plus_one) < 2:
                    month_plus_one = '0' + month_plus_one
                if format_time[5:7] == date[5:7]:
                    if int(format_time[8:10]) <= int(date[8:10]) <= max_day[format_time[5:7]]:
                        return cls
                    else:
                        raise AppointmentDateError
                elif date[5:7] == month_plus_one:
                    if 0 < int(format_time[8:10]) <= int(date[8:10]):
                        return cls
                    else:
                        raise AppointmentDateError
                else:
                    raise AppointmentDateError
            else:
                raise AppointmentDateError
        else:
            raise AppointmentDateError

    @classmethod
    def time_set(cls, time_):
        i = 0
        size = len(time_)
        pattern = re.compile(r'[0-9][0-9]:[0-9][0-9]-[0-9][0-9]:[0-9][0-9]')
        if size < i + 11:
            raise TimeSetError
        while i + 11 <= size:
            if i + 11 < size:
                if not time_[i+11] == '-':
                    raise TimeSetError
            if not pattern.match(time_[i:i+11]):
                raise TimeSetError
            i += 12
        return cls

    @classmethod
    def name(cls, name):
        s = '字' * 4
        if 1 < len(name) <= len(s):
            return cls
        raise UserNameError

    @classmethod
    def shop_name(cls, shop_name):  # 检查什么
        return cls

    @classmethod
    def phone(cls, phone):
        prefix = ['130', '131', '132',
                  '133', '134', '135',
                  '136', '137', '138',
                  '139', '150', '151',
                  '152', '153', '155',
                  '156', '157', '158',
                  '159', '170', '180',
                  '181', '182', '183',
                  '184', '185', '186',
                  '187', '188', '189']
        if len(phone) == 11:
            if phone.isdigit():
                if phone[:3] in prefix:
                    return cls
                else:
                    raise PhoneError
            else:
                raise PhoneError
        else:
            raise PhoneError

    @classmethod
    def distance(cls, distance):
        if not type(distance) == int:
            raise DistanceError
        return cls

    @classmethod
    def remark(cls, remark):
        s = '字'*26
        if not len(remark) <= len(s):
            raise RemarkError
        return cls

    @classmethod
    def password(cls, password):
        """
        len > 8
        contains numbers and words at the same time.
        don't contains special characters.
        {'.','_','@','$'}
        :param password:
        :return:
        """
        if len(password) < 8:
            raise PasswordError
        _, *p = password
        p.append(_)
        p = set(p)
        num = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
        words = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D',
                 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                 'Y', 'Z'}
        char = {'.', '_', '@', '$'}
        if p & num and p & words:
            if p - num - words - char:
                raise PasswordError
            else:
                return cls
        else:
            raise PasswordError

    @classmethod
    def appt_time(cls, time_):
        pattern_quick = re.compile(r'[0-9][0-9][0-9][0-9].[0-9][0-9].[0-9][0-9];[0-9][0-9]:[0-9][0-9]')
        pattern_appt = re.compile(r'[0-9][0-9][0-9][0-9].[0-9][0-9].[0-9][0-9];[0-9][0-9]:[0-9][0-9]-[0-9][0-9]:[0-9][0-9]')
        match_quick = pattern_quick.match(time_)
        match_appt = pattern_appt.match(time_)
        #first step:pattern match
        if match_quick or match_appt:
            return cls
        else:
            raise AppointmentTimeError

    @classmethod
    def request(cls, request, keys):
        if not request.method == 'POST' or not request.POST:
            raise RequestMethodError
        re_keys = request.POST.keys()
        data = {}
        for key in keys:
            if not key in re_keys:
                raise RequestKeyError
            else:
                if not request.POST[key] and not key == 'remark':  # empty string not None, except remark
                    raise PassValueError
                data[key] = request.POST[key]
        return data

    @classmethod
    def address(cls, address_):  # 不好检测
        if not address_:
            raise AddressError
        return cls

    @classmethod
    def order_conflict(cls, order: dict):
        """
        处理订单冲突
        :return:
        """
        pass

    @classmethod
    def profile(cls, image: str):
        return cls






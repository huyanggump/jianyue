from robust.checker import *
from robust.exception import *
from django.http import HttpResponse
from utilities.network import encode
from appointment.appt import notify_cus_order_accepted
from order.orders import OrderProxy
from barber.barbers import BarberProxy, BarbersManager
from shop.shops import ShopsManager
import time
#view layer


def accepted_order(request):
    result = {'code': 100, 'log': 'order accepted success'}
    re_data = None
    try:
        data = Checker.request(request, ['orderID', 'phone', 'distance'])
        format_time = time.strftime('%Y.%m.%d;%H:%M', time.localtime(time.time()))
        order = OrderProxy(int(data['orderID']))
        if order.accepted:
            raise OrderHasAccepted
        order = order.update(bar_phone=data['phone'], time_=format_time, accepted=True).get_dict()
        barber = BarberProxy(data['phone'])
        order['distance'], order['shop'], order['address'] = data['distance'], barber.shop, barber.address
        notify_cus_order_accepted(order)
    except JianyueError as e:
        result = e.info
    finally:
        result['data'] = re_data
        return HttpResponse(encode(result))


def register(request):
    result = {'code': 100, 'log': 'register success'}
    re_data = None
    try:
        data = Checker.request(request, ['phone', 'name', 'sex', 'password', 'shop', 'time'])
        try:
            _ = BarberProxy(data['phone'])
        except BarberDoesNotExistError:
            BarbersManager.add_barber(phone=data['phone'], name=data['name'],
                                      sex=data['sex'], password=data['password'],
                                      shop=data['shop'], time_=data['time'])
        else:
            raise BarberHasRegister
    except JianyueError as e:
        result = e.info
    finally:
        result['data'] = re_data
        return HttpResponse(encode(result))


def is_register(request):
    result = {'code': 504, 'log': 'Barber has register'}  # BarhasRegister
    re_data = None
    try:
        data = Checker.request(request, ['phone'])
        _ = BarberProxy(data['phone'])
    except JianyueError as e:
        result = e.info
    except Exception:
        result['code'] = 101
        result['log'] = 'Internal error'
    finally:
        result['data'] = re_data
        return HttpResponse(encode(result))


def get_near_shop(request):
    result = {'code': 100, 'log': 'barber list has returned'}
    re_data = None
    try:
        data = Checker.request(request, ['longitude', 'latitude'])
        shops = ShopsManager.get_near_shop(longitude=float(data['longitude']),
                                           latitude=float(data['latitude']), range_=1500)
        re_data = shops
    except JianyueError as e:
        result = e.info
    finally:
        result['data'] = re_data
        return HttpResponse(encode(result))


def login(request):
    result = {'code': 100, 'log': 'login success'}
    re_data = None
    try:
        data = Checker.request(request, ['phone', 'password'])
        BarberProxy(data['phone']).match(data['password'])
    except JianyueError as e:
        result = e.info
    finally:
        result['data'] = re_data
        return HttpResponse(encode(result))


def set_appt_time(request):
    result = {'code': 100, 'log': 'time set success'}
    re_data = None
    try:
        data = Checker.request(request, ['phone', 'time'])
        BarberProxy(data['phone']).set_appt_time(data['time'])
    except JianyueError as e:
        result = e.info
    finally:
        result['data'] = re_data
        return HttpResponse(encode(result))


def update_name(request):
    result = {'code': 100, 'log': "Barber's name update success!"}
    re_data = None
    try:
        data = Checker.request(request, ['phone', 'name'])
        BarberProxy(phone=data['phone']).name = data['name']
    except JianyueError as e:
        result = e.info
    finally:
        result['data'] = re_data
        return HttpResponse(encode(result))


def update_sex(request):
    result = {'code': 100, 'log': "Barber's sex update success!"}
    re_data = None
    try:
        data = Checker.request(request, ['phone', 'sex'])
        BarberProxy(phone=data['phone']).sex = data['sex']
    except JianyueError as e:
        result = e.info
    finally:
        result['data'] = re_data
        return HttpResponse(encode(result))


##
def update_profile(request):
    result = {'code': 100, 'log': "return infomation"}
    re_data = None
    try:
        data = Checker.request(request, ['phone'])
        barber = BarberProxy(phone=data['phone'])
        barber.profile = 'profile/barber/' + barber.phone + '.png'
        re_data = {
            'key': barber.profile,
            'bucket_name': 'jianyue-img',
            'access_key_id': 'DS1sGprn39SnhFDV',
            'access_key_secret': 'dFmlLMHapOfyUKTDeeUFCp7M64U1aD',
        }
    except JianyueError as e:
        result = e.info
    finally:
        result['data'] = re_data
        return HttpResponse(encode(result))
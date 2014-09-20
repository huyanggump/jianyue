from robust.checker import Checker
from robust.exception import *
from django.http import HttpResponse
from customer.customers import CustomersManager, CustomerProxy
from barber.barbers import BarbersManager
from order.orders import OrdersManager, OrderProxy
from appointment.appt import *
from utilities.network import encode


def quick_appt(request):
    result = {'code': 100, 'log': '已将订单发送至理发师端'}
    re_data = None
    try:
        data = Checker.request(request, ['phone', 'name', 'longitude', 'latitude', 'sex'])
        try:
            _ = CustomerProxy(data['phone'])
        except CustomerDoesNotExistError:
            CustomersManager.add_customer(phone=data['phone'], name=data['name'], sex=data['sex'])
        order = OrdersManager.add_order(cus_phone=data['phone'])
        barbers, dis = BarbersManager.get_near_barber(longitude=float(data['longitude']),
                                                      latitude=float(data['latitude']), range_=1500)
        push_order_to_barber(order=order, barbers=barbers, dis_list=dis)
    except JianyueError as e:
        result = e.info
    finally:
        result['data'] = re_data
        return HttpResponse(encode(result))


def normal_appt(request):
    result = {'code': 100, 'log': '返回理发师列表'}
    re_data = None
    try:
        data = Checker.request(request, ['longitude', 'latitude', 'date'])
        barbers, dis_list = BarbersManager.get_near_barber(longitude=float(data['longitude']),
                                                           latitude=float(data['latitude']), range_=1500)
        barbers = process_time(barbers=barbers, date=data['date'])
        l = len(barbers)
        for i in range(0, l):
            barbers[i]['distance'] = dis_list[i]
        barbers.sort(key=lambda d: d['distance'])
        if not barbers:
            raise NoBarberHasRegister
        re_data = barbers
    except JianyueError as e:
        result = e.info
    finally:
        result['data'] = re_data
        return HttpResponse(encode(result))


def submit_order(request):
    result = {'code': 100, 'log': '已通知理发师'}
    re_data = None
    try:
        data = Checker.request(request, ['barphone', 'cusphone', 'cusname', 'sex',
                                         'time', 'distance', 'hairstyle', 'remark'])
        #try:
        #    _ = CustomerProxy(data['cusphone'])
        #except CustomerDoesNotExistError:
        CustomersManager.add_customer(phone=data['cusphone'], name=data['cusname'], sex=data['sex'])

        time_conflict(phone=data['cusphone'], time_=data['time'])  # ??

        time_ = calculate_order_time(hairstyle=data['hairstyle'], time_=data['time'])

        order = OrdersManager.add_order(cus_phone=data['cusphone'], bar_phone=data['barphone'],
                                        time_=time_, hairstyle=data['hairstyle'],
                                        remark=data['remark'], accepted=True).get_dict()
        order.pop('accepted')
        push_msg(alias=order['barphone'], msg=order)
    except JianyueError as e:
        result = e.info
    finally:
        result['data'] = re_data
        return HttpResponse(encode(result))


def is_register(request):
    result = {'code': 100, 'log': '用户已注册，返回用户信息'}
    re_data = None
    try:
        data = Checker.request(request, ['phone'])
        customer = CustomerProxy(data['phone'])
        re_data = customer.get_dict()
    except JianyueError as e:
        result = e.info
    finally:
        result['data'] = re_data
        return HttpResponse(encode(result))


def get_barber(request):
    result = {'code': 100, 'log': '返回请求理发师信息'}
    re_data = None
    try:
        data = Checker.request(request, ['phone', 'date'])
        re_data = process_time(barbers=[BarberProxy(data['phone'])], date=data['date'])[0]
    except JianyueError as e:
        result = e.info
    finally:
        result['data'] = re_data
        return HttpResponse(encode(result))
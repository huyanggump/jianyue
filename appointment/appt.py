__author__ = 'boyang'
from order.orders import OrdersManager, OrderProxy
from barber.barbers import HairstyleProxy, BarberProxy
from utilities.push import push_msg
from robust.exception import OrderTimeClash, PushError
from robust.checker import Checker


def notify_cus_order_accepted(order):
    order.pop('accepted')
    order.pop('time')
    push_msg(alias=order['cusphone'], msg=order)


def push_order_to_barber(*, order: OrderProxy, barbers: [BarberProxy], dis_list):  # order需不需要做处理
    size = len(dis_list)
    error = 0
    for i in range(0, size):
        _ = order.get_dict()
        o = {}
        o['phone'] = _['cusphone']
        o['name'] = _['cusname']
        o['distance'] = dis_list[i]
        try:
            push_msg(alias=barbers[i].phone, msg=o)
        except Exception:
            error += 1
    if error:
        raise PushError


def process_time(*, barbers: [BarberProxy], date: str) -> [dict]:  # 最好做一个testing
    Checker.appt_date(date)
    re_barbers = []
    for barber in barbers:
        bar_time = barber.time.split('-')
        start = date + ';' + bar_time[0] + '-' + bar_time[0]
        end = date + ';' + bar_time[-1] + '-' + bar_time[-1]
        orders = OrdersManager.get_by_time(start=start, end=end)

        #
        his_order = [order for order in orders if order.bar_phone == barber.phone]
        #
        for order in his_order:
            ord_time = order.time.split(';')[1].split('-')
            if not ord_time[0] in bar_time:
                bar_time.append(ord_time[0])
            else:
                bar_time.remove(ord_time[0])
            if not ord_time[1] in bar_time:
                bar_time.append(ord_time[1])
            else:
                bar_time.remove(ord_time[1])
            bar_time.sort()
        time_ = ''
        for t in bar_time:
            time_ += t
            time_ += '-'
        time_ = time_[:-1]
        b = barber.get_dict()
        b['time'] = time_
        re_barbers.append(b)
    return re_barbers


def time_conflict(*, phone: str, time_: str):
    orders = OrdersManager.get_by_cus(phone)
    for order in orders:
        if order.time and order.time[0:16] == time_:
            raise OrderTimeClash


def calculate_order_time(*, hairstyle, time_):
    cut_time = HairstyleProxy(hairstyle).time
    suffix = cut_time + int(time_[14:16])
    hour = str(int(time_[11:13]) + suffix // 60)
    mint = str(suffix - 60 * (suffix // 60))
    if len(hour) < 2:
        hour = '0' + hour
    if len(mint) < 2:
        mint = '0' + mint
    time_ += '-' + hour + ':' + mint
    return time_


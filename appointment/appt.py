__author__ = 'boyang'
from order.orders import OrdersManager, OrderProxy
from barber.barbers import HairstyleProxy, BarberProxy
from utilities.push import push_msg
from robust.exception import OrderTimeClash, PushError
from robust.checker import Checker
'''下面一行是junhui增加的'''
from order.models import *


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


'''written by junhui'''

def cal_time(start,end):#计算两个时间点相差的分钟数
    start_hour = start.split(':')[0]
    start_min = start.split(':')[1]
    end_hour = end.split(':')[0]
    end_min = end.split(':')[1]
    minutes = (end_hour - start_hour) * 60 + (end_min - start_min)
    return minutes

def cal_hair_time(hair:str):#查询出此发型所需分钟数
    hairstyle = Hairstyle.objects.get(hairstyle_name = hair)
    return hairstyle.hairstyle_time

def order_clash(*, bar_phone: str, time_: str,hair: str):
    barber = Barber.objects.get(barber_phone = bar_phone)
    ord_nums = Order.objects.filter(ord_barber_id = barber.barber_id).count()#属于此理发师的订单数目
    if ord_nums == 0:
        print('') #如果此理发师的订单数目为零，那么显然不会冲突。(print没有意义，但是不知道写啥，就写了这条语句。)
    else:
        ord_L = Order.objects.filter(ord_barber_id = barber.barber_id).values('ord_time')
        for ord_D in ord_L: #遍历每一条订单记录来检测是否存在冲突
            date = ord_D['ord_time'].split(';')[0]
            start_time = ord_D['ord_time'].split(';')[1].split('-')[0]
            end_time = ord_D['ord_time'].split(';')[1].split('-')[1]
            checking_date = time_.split(';')[0]
            checking_time = time_.split(';')[1]
            if checking_date == date: #预约日期相符的话继续比较
                if start_time <= checking_time < end_time:
                    raise OrderTimeClash
                elif ( checking_time<start_time and cal_time(checking_time,start_time) < cal_hair_time(hair) ):
                    raise OrderTimeClash
                else: #时间不冲突，则继续比较下面的订单
                    print('')
            else: #预约日期不相符的话此条订单不会相冲突，继续比较下面的订单
                print('')

    """
    by junhui
    compare the bar_phone and time_ in database, if time clash,
    raise OrderTimeClash Error.
    :raise OrderTimeClash
    :param bar_phone:
    :param time_:
    :return:
    """

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


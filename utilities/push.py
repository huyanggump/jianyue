__author__ = 'boyang'
import json
import jpush
from robust.exception import *
from jpush import JPushFailure, Unauthorized
_app_key = u'70a3572c60d2e498ec309fef'
_master_secret = u'2046065419a447373b2474f9'


def push_msg(*, alias: str, msg: dict):
    try:
        jpush_ = jpush.JPush(_app_key, _master_secret)
        push = jpush_.create_push()
        push.audience = jpush.audience(jpush.alias(alias))
        msg = json.dumps(msg)
        push.message = jpush.message(msg_content=msg)
        push.platform = jpush.all_
        push.send()
    #terrible
    except JPushFailure:
        raise PushError
    except Unauthorized:
        raise PushError
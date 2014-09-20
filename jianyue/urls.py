from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url('^appointment/quick/$', 'customer.views.quick_appt'),
    url('^appointment/normal/$', 'customer.views.normal_appt'),
    url('^appointment/normal/submit-order/$', 'customer.views.submit_order'),
    url('^appointment/get/barber/$', 'customer.views.get_barber'),
    url('^customer/isregister/$', 'customer.views.is_register'),
    url('^appointment/quick/order-accepted/$', 'barber.views.accepted_order'),
    url('^barber/register/$', 'barber.views.register'),
    url('^barber/isregister/$', 'barber.views.is_register'),
    url('^get-near-shop/$', 'barber.views.get_near_shop'),
    url('^barber/login/$', 'barber.views.login'),
    url('^barber/set-time/$', 'barber.views.set_appt_time'),
    url('^test/$', 'jianyue.views.test'),

    url('^test/player/$', 'jianyue.views.player'),
    url('^test/player/door/$', 'jianyue.views.door'),
    url('^test/player/login/$', 'jianyue.views.login'),
    url('^bug/', 'jianyue.views.bug'),
)
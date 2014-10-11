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

    url('^update/customer/name/$', 'customer.views.update_name'),
    url('^update/customer/sex/$', 'customer.views.update_sex'),
    url('^update/customer/profile/$', 'customer.views.update_profile'),

    url('^update/barber/name/$', 'barber.views.update_name'),
    url('^update/barber/sex/$', 'barber.views.update_sex'),
    url('^update/barber/profile/$', 'barber.views.update_profile'),
)
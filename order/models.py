from django.db import models
from barber.models import Barber
from customer.models import Customer
from barber.models import Hairstyle


class Order(models.Model):
    ord_id = models.AutoField(primary_key=True)
    ord_barber_id = models.ForeignKey(Barber, db_column='ord_barber_id', null=True)
    ord_cus_id = models.ForeignKey(Customer, db_column='ord_cus_id')
    ord_hairstyle_id = models.ForeignKey(Hairstyle, db_column='ord_hairstyle_id', null=True, blank=True)
    ord_time = models.CharField(max_length=30, null=True)
    ord_remark = models.TextField(blank=True, null=True)
    ord_is_acc = models.BooleanField(default=False)

    def __unicode__(self):
        return 'cus:{0}, bar:{1}, time:{2}'.format(self.ord_cus_id.cus_name,
                                                   self.ord_barber_id.barber_name,
                                                   self.ord_time)

    class Meta:
        db_table = 'order_ta'

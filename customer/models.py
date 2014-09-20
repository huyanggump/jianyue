from django.db import models


class Customer(models.Model):
    cus_id = models.AutoField(primary_key=True)
    cus_name = models.CharField(max_length=20)
    cus_phone = models.CharField(max_length=11, unique=True)
    cus_sex = models.CharField(max_length=6)

    def __unicode__(self):
        return self.cus_name

    class Meta:
        db_table = 'customer_ta'
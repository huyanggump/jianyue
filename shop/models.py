from django.db import models


class Shop(models.Model):
    shop_id = models.AutoField(primary_key=True)
    shop_name = models.CharField(max_length=15)
    shop_pass = models.CharField(max_length=32)
    shop_phone = models.CharField(max_length=11)
    shop_long = models.FloatField(null=True)
    shop_lati = models.FloatField(null=True)
    shop_add = models.CharField(max_length=70,null=True)

    class Meta:
        db_table = 'shop_ta'







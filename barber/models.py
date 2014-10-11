from django.db import models
from shop.models import Shop

# Model layer


class Barber(models.Model):
    barber_id = models.AutoField(primary_key=True)
    barber_shop_id = models.ForeignKey(Shop, db_column='barber_shop_id', null=True)
    barber_name = models.CharField(max_length=20)
    barber_phone = models.CharField(max_length=11, unique=True)
    barber_pass = models.CharField(max_length=32)
    barber_sex = models.CharField(max_length=6, null=True)
    free_time = models.CharField(max_length=100, null=True)
    barber_profile = models.CharField(max_length=100, null=True)

    def __unicode__(self):
        return self.barber_name

    class Meta:
        db_table = 'barber_ta'


class Hairstyle(models.Model):
    hairstyle_id = models.AutoField(primary_key=True)
    hairstyle_name = models.CharField(max_length=20, unique=True)
    hairstyle_time = models.IntegerField(max_length=180)

    def __unicode__(self):
        return self.barber_name

    class Meta:
        db_table = 'hairstyle_ta'







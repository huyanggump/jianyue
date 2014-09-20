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
    free_time = models.CharField(max_length=70, null=True)

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


class Price(models.Model):
    price_id = models.AutoField(primary_key=True)
    price_barber_id = models.ForeignKey(Barber, db_column='price_barber_id')
    price_hairstyle_id = models.ForeignKey(Hairstyle, db_column='price_hairstyle_id')
    price = models.FloatField()

    def __unicode__(self):
        return str(self.price)

    class Meta:
        db_table = 'price_ta'
        unique_together = ("price_barber_id", "price_hairstyle_id")





from django.db import models
from django.utils import timezone
import datetime

# Create your models here.

    #primary key dates or duplicate dates ?
    # incorrect info edit option ?
    # edit option only to admin or who ?
    # %wt ?
class layer(models.Model):
    layer_no = models.SmallIntegerField(primary_key=True)
    occupied = models.BooleanField()

    def __str__(self):
        return 'Layer '+str(self.layer_no)+" "+str(self.occupied)[0]

class chicks(models.Model):
    batch_no = models.PositiveSmallIntegerField(primary_key=True)
    date = models.DateTimeField(default=timezone.now())
    total_birds = models.PositiveIntegerField(default=0)
    active = models.BooleanField()

    def __str__(self):
        return 'Batch '+str(self.batch_no)+" "+str(self.active)[0]


class chicks_data(models.Model):
    batch_no = models.ForeignKey(chicks,on_delete=models.DO_NOTHING)
    date = models.DateTimeField(default=timezone.now())
    total_birds = models.PositiveIntegerField(default=0)
    mortality = models.PositiveIntegerField(default=0)
    sold = models.PositiveIntegerField(default=0)
    def __str__(self):
        return str(self.batch_no) +" "+ f"{self.date.strftime('%d-%m-%y')}"

class feed_chicks(models.Model):
    batch_no = models.ForeignKey(chicks,on_delete=models.DO_NOTHING)
    date = models.DateTimeField(default=timezone.now())
    received = models.PositiveIntegerField(default=0)
    meter_reading = models.PositiveIntegerField(default=0)
    used = models.IntegerField(default=0)
    gram_per_bird = models.FloatField(default=0)
    def __str__(self):
        return str(self.batch_no) +" "+ f"{self.date.strftime('%d-%m-%y')}"

class bt_lyr(models.Model):
    layer_no = models.ForeignKey(layer,on_delete=models.DO_NOTHING)
    batch_no = models.ForeignKey(chicks,on_delete=models.DO_NOTHING)
    date = models.DateTimeField(default=timezone.now())
    active = models.BooleanField()
    
    class Meta:
        unique_together = ('batch_no','layer_no',)

    def __str__(self):
        return str(self.layer_no)+" "+str(self.batch_no)

class feed_hen(models.Model):
    bt_lyr_no = models.ForeignKey(bt_lyr,on_delete=models.DO_NOTHING)
    date = models.DateTimeField(default=timezone.now())
    received = models.PositiveIntegerField(default=0)
    meter_reading = models.PositiveIntegerField(default=0)
    used = models.IntegerField(default=0)
    gram_per_bird = models.FloatField(default=0)
    def __str__(self):
        return str(self.bt_lyr_no) +" "+ f"{self.date.strftime('%d-%m-%y')}"

class eggs(models.Model):
    #eggs

    bt_lyr_no =  models.ForeignKey(bt_lyr,on_delete=models.DO_NOTHING)
    date_time = models.DateTimeField(editable=True,default=timezone.now())
    normal = models.PositiveIntegerField(default=0)
    small = models.PositiveIntegerField(default=0)
    big = models.PositiveIntegerField(default=0)
    broken = models.PositiveIntegerField(default=0)
    damage = models.PositiveIntegerField(default=0)
    day_total = models.PositiveIntegerField(default=0)
    production = models.FloatField(default=0)
    closing = models.PositiveIntegerField(default=0)

    #delivery

    delivery_normal = models.PositiveIntegerField(default=0)
    delivery_big = models.PositiveIntegerField(default=0)
    delivery_small = models.PositiveIntegerField(default=0)
    delivery_broken = models.PositiveIntegerField(default=0)
    to_gate = models.PositiveIntegerField(default=0)
    spoiled = models.PositiveIntegerField(default=0)

    #birds

  
    total_birds = models.PositiveIntegerField(default=0)
    sold = models.PositiveIntegerField(default=0)
    mortality = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return str(self.bt_lyr_no) +" "+f"{self.date_time.strftime('%d-%m-%y')}"
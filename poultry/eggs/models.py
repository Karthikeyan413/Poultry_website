from enum import unique
from pyexpat import model
from django.db import models
import datetime

# Create your models here.

    #primary key dates or duplicate dates ?
    # incorrect info edit option ?
    # edit option only to admin or who ?
    # %wt ?
class bt_lyr(models.Model):
    batch_no = models.PositiveSmallIntegerField(unique=True)
    layer_no = models.PositiveSmallIntegerField()

    def __str__(self):
        return 'B'+str(self.batch_no)+" L"+str(self.layer_no)
    
class eggs(models.Model):
    batch_no = models.ForeignKey(bt_lyr,on_delete=models.CASCADE)
    date_time = models.DateField(editable=True,unique=True,default=datetime.datetime.now().date())
    normal = models.PositiveIntegerField(default=0)
    small = models.PositiveIntegerField(default=0)
    big = models.PositiveIntegerField(default=0)
    broken = models.PositiveIntegerField(default=0)
    damage = models.PositiveIntegerField(default=0)
    day_total = models.PositiveIntegerField(default=0,editable=False)
    production = models.FloatField(default=0)
    delivery = models.PositiveIntegerField(default=0)
    to_gate = models.PositiveIntegerField(default=0)
    spoiled = models.PositiveIntegerField(default=0)
    closing = models.PositiveIntegerField(default=0,editable=False)
    total_birds = models.PositiveIntegerField(default=0,editable=False)
    sold = models.PositiveIntegerField(default=0)
    mortality = models.PositiveSmallIntegerField(default=0)
    # production greater than 200 ?
    # Negative Values Posible in closing ?
    # initial entry closing & birds ?
    # paper rate ?
    def __str__(self):
        return f"{self.date_time.strftime('%d-%m-%Y')}"

    def save(self,*args,**kwargs):
        if(eggs.objects.all().exists()):
            self.day_total = self.normal + self.small + self.big + self.broken
            date_time = self.date_time - datetime.timedelta(days=1)
            # closing_prev = eggs.objects.get(date_time =  date_time).closing
            # self.closing = closing_prev + self.day_total - self.delivery - self.to_gate - self.spoiled
            # total_birds_prev =  eggs.objects.get(date_time =  date_time).total_birds
            # self.total_birds = total_birds_prev - self.mortality - self.sold
            # self.production = round(((self.day_total/self.total_birds)*100),3)

            super(eggs,self).save(*args,**kwargs)
        else:
            self.date_time = datetime.datetime.now()
            super(eggs,self).save(*args,**kwargs)
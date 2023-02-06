from django.db import models
import datetime

# Create your models here.

    #primary key dates or duplicate dates ?
    # incorrect info edit option ?
    # edit option only to admin or who ?
    # %wt ?
class layer(models.Model):
    layer_no = models.SmallIntegerField(primary_key=True)
    occupied = models.BooleanField()

class chicks(models.Model):
    batch_no = models.PositiveSmallIntegerField(primary_key=True)
    date = models.DateField(default=datetime.datetime.now().date())
    total_birds = models.PositiveIntegerField(default=0)
    active = models.BooleanField()

# class bt_lyr(models.Model):
#     batch_no = models.PositiveSmallIntegerField()
#     layer_no = models.PositiveSmallIntegerField()

#     class Meta:
#         unique_together = ('batch_no','layer_no',)
#     def __str__(self):
#         return 'Batch '+str(self.batch_no)+" Layer "+str(self.layer_no)

class chicks_data(models.Model):
    batch_no = models.ForeignKey(chicks,on_delete=models.DO_NOTHING)
    date = models.DateField(default=datetime.datetime.now().date())
    total_birds = models.PositiveIntegerField(default=0)
    mortality = models.PositiveIntegerField(default=0)
    sold = models.PositiveIntegerField(default=0)


class feed_chicks(models.Model):
    batch_no = models.ForeignKey(chicks,on_delete=models.DO_NOTHING)
    # date = models.DateField(default=datetime.datetime.now().date())
    received = models.PositiveIntegerField(default=0)
    meter_reading = models.PositiveIntegerField(default=0)
    used = models.IntegerField(default=0)
    gram_per_bird = models.FloatField(default=0)

# class feed_hen(models.Model):
#     bt_lyr = models.ForeignKey(bt_lyr,on_delete=models.DO_NOTHING)
#     layer_no = models.ForeignKey(layer,on_delete=models.DO_NOTHING)
#     received = models.PositiveIntegerField()
#     meter_reading = models.PositiveIntegerField()
#     used = models.IntegerField()
#     gram_per_bird = models.FloatField()

# class eggs(models.Model):
#     batch_no = models.ForeignKey(bt_lyr,on_delete=models.CASCADE)
#     date_time = models.DateField(editable=True,default=datetime.datetime.now().date())
#     normal = models.PositiveIntegerField(default=0)
#     small = models.PositiveIntegerField(default=0)
#     big = models.PositiveIntegerField(default=0)
#     broken = models.PositiveIntegerField(default=0)
#     damage = models.PositiveIntegerField(default=0)
#     day_total = models.PositiveIntegerField(default=0,editable=False)
#     production = models.FloatField(default=0)
#     delivery = models.PositiveIntegerField(default=0)
#     to_gate = models.PositiveIntegerField(default=0)
#     spoiled = models.PositiveIntegerField(default=0)
#     closing = models.PositiveIntegerField(default=0,editable=False)
#     total_birds = models.PositiveIntegerField(default=0,editable=False)
#     sold = models.PositiveIntegerField(default=0)
#     mortality = models.PositiveSmallIntegerField(default=0)
#     # production greater than 200 ?
#     # Negative Values Posible in closing ?
#     # initial entry closing & birds ?
#     # paper rate ?
#     def __str__(self):
#         return f"{self.date_time.strftime('%d-%m-%Y')}"

#     def save(self,*args,**kwargs):
#         if(eggs.objects.all().exists()):
#             self.day_total = self.normal + self.small + self.big + self.broken
#             #date_time = self.date_time - datetime.timedelta(days=1)
#             #closing_prev = eggs.objects.get(date_time =  date_time).closing
#             closing_prev = eggs.objects.last().closing
#             self.closing = closing_prev + self.day_total - self.delivery - self.to_gate - self.spoiled
#             #total_birds_prev =  eggs.objects.get(date_time =  date_time).total_birds
#             total_birds_prev =  eggs.objects.last().total_birds
#             self.total_birds = total_birds_prev - self.mortality - self.sold
#             self.production = round(((self.day_total/self.total_birds)*100),3)

#             super(eggs,self).save(*args,**kwargs)
#         else:
#             self.date_time = datetime.datetime.now()
#             super(eggs,self).save(*args,**kwargs)
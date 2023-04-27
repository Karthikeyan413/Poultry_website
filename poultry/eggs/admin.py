from django.contrib import admin
from eggs.models import chicks,feed_chicks,chicks_data,layer,eggs,bt_lyr,feed_hen,delivery


# Register your models here.
admin.site.register(layer)
admin.site.register(chicks)
admin.site.register(chicks_data)
admin.site.register(feed_chicks)
admin.site.register(bt_lyr)
admin.site.register(eggs)
admin.site.register(delivery)
admin.site.register(feed_hen)

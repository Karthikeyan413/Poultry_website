from django.contrib import admin
from eggs.models import chicks,chicks_data,feed_chicks,layer


# Register your models here.
admin.site.register(layer)
admin.site.register(chicks)
admin.site.register(chicks_data)
admin.site.register(feed_chicks)

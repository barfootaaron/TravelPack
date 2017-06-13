from django.contrib import admin

from .models import Trip, TripType, PaymentType, Order

# Register your models here.
admin.site.register(Trip)
admin.site.register(TripType)
admin.site.register(PaymentType)
admin.site.register(Order)


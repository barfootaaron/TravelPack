from django.contrib import admin

from .models import Trip, TripType, PaymentType, Order, Customer, TripOrder, TripReview, WishList

# Register your models here.
admin.site.register(Trip)
admin.site.register(TripType)
admin.site.register(PaymentType)
admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(TripOrder)
admin.site.register(TripReview)
admin.site.register(WishList)


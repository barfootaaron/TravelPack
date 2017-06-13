import datetime

from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse
from django.utils import timezone
from sorl.thumbnail import ImageField

class TripType(models.Model):                      
    """
    purpose: Instantiates a trip type
    args: Extends the models.Model Django class
    returns: (None): N/A
    """   
    trip_type_name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.trip_type_name

    def get_absolute_url(self):
        return "/trip_type_trips/{}".format(self.id)

class Trip(models.Model):
    """
    purpose: Instantiates a trip
    args: Extends the models.Model Django class
    returns: (None): N/A
    """   
    seller = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
    )
    trip_type = models.ForeignKey(TripType)
    title = models.CharField(max_length=255)
    num_of_nights = models.IntegerField()
    location = models.TextField(blank=True, null=False)
    description = models.TextField(blank=True, null=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    quantity = models.IntegerField()
    quantity_sold = models.IntegerField(default=0)
    trip_img = models.ImageField(blank=True, null=True) 

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/single_trip/{}".format(self.id)


class Customer(models.Model):
    """
    purpose: Instantiates a customer
    args: Extends the models.Model Django class
    returns: (None): N/A
    """   
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.IntegerField(default=0, blank=True, null=True)
    street_address = models.CharField(max_length=255, blank=True, null=True)




class PaymentType(models.Model):
    """
    purpose: Instantiates a payment type
    args: Extends the models.Model Django class
    returns: (None): N/A
    """   
    payment_type_name = models.CharField(max_length=15)
    account_number = models.IntegerField()
    customer = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
    )

    class Meta:
        ordering = ('payment_type_name',)

    def __str__(self):
        return self.payment_type_name

class Order(models.Model):
    """
    purpose: Instantiates an order
    args: Extends the models.Model Django class
    returns: (None): N/A
    """
    order_date = models.DateTimeField('Order Date', null=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.PROTECT, null=True)
    trips = models.ManyToManyField(Trip, through="TripOrder")
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ('order_date',)

class TripOrder(models.Model):
    """
    purpose: Instantiates an instance of a trip on an order
    args: Extends the models.Model Django class
    returns: (None): N/A
    """   
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


    class Meta:
        ordering = ('trip',)

    def __str__(self):
        return self.trip.title



class TripOpinion(models.Model):
    """
    purpose: Store trip likes and dislikes
    args: extends the imported Django model class 
    returns: (None): N/A
    """
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    opinion = models.IntegerField(default=0)







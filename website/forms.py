from django.contrib.auth.models import User
from django import forms
from website.models import Trip, PaymentType, Order, Customer


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

class TripForm(forms.ModelForm): 

    class Meta:
        model = Trip
        fields = ('title', 'num_of_nights', 'description', 'price', 'quantity', 'trip_type', 'trip_img', 'location',)

class PaymentTypeForm(forms.ModelForm):

	class Meta:
		model = PaymentType
		fields = ('payment_type_name', 'account_number')

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('payment_type',)
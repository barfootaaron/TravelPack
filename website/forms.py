from django.contrib.auth.models import User
from django import forms
from website.models import Trip, PaymentType, Order, Customer, TripReview


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

class PaymentTypeForm(forms.ModelForm):

	class Meta:
		model = PaymentType
		fields = ('payment_type_name', 'account_number')

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('payment_type',)

class TripReviewForm(forms.ModelForm):

    class Meta:
        model = TripReview
        fields = ('trip', 'rating', 'review_text')         
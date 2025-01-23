from django import forms
from .models import User, Apartment, Address, Image
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'status']

class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = ['numberRooms', 'size', 'floor', 'price']

class ApartmentMediatorForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = ['numberRooms', 'size', 'floor', 'price', 'charge']

class ImagesForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['city', 'street', 'buildingNumber']
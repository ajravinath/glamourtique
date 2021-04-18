from django.forms import *
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            'customer': Select(attrs={'class': 'form-control'}),
            'products': SelectMultiple(attrs={'class': 'form-control'}),
            'status': Select(attrs={'class': 'form-control'}),
            'note': Textarea(attrs={'class': 'form-control'}),
        }


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'price': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'}),
            'category': Select(attrs={'class': 'form-control'}),
            'tags': SelectMultiple(attrs={'class': 'form-control'}),
        }


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        widgets = {
            # 'user': Select(attrs={'class': 'form-control'}),
            'name': TextInput(attrs={'class': 'form-control'}),
            'phone': TextInput(attrs={'class': 'form-control'}),
            'email': TextInput(attrs={'class': 'form-control'}),
        }


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AuthenticateUserForm(AuthenticationForm):
    class Meta:
        model = User

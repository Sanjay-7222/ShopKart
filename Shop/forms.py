from django.contrib.auth.forms import UserCreationForm
from .models import *   
from django import forms 
from django.forms import ModelForm

class CustomUserForm(UserCreationForm):
    username = forms.CharField(widget = forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Username'}))
    email = forms.EmailField(widget = forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Email Address'}))
    password1 = forms.CharField(widget = forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Your Password','id' : 'password'}))
    password2 = forms.CharField(widget = forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Confirm Password', 'id' : 'confirmpassword'}))
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class CheckoutForm(ModelForm):
    class Meta:
        model = Chekout
        fields = ['user_address','phone_no',"quantity"]
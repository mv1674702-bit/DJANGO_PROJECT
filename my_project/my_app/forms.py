from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Item

# Register form
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Item form
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description']
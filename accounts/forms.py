from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Item, Review

class UserRegistrationForm(UserCreationForm):
    is_buyer = forms.BooleanField(required=False)
    is_seller = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_buyer', 'is_seller']

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'price', 'category', 'quantity','image_url']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']


class OrderReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }
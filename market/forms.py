# market/forms.py
from django import forms
from .models import MarketData, Category
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email',)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)

class MarketDataForm(forms.ModelForm):
    class Meta:
        model = MarketData
        fields = ['product_name', 'price', 'quantity', 'vendor_details', 'category', 'tags', 'image', 'document']

class MarketDataSearchForm(forms.Form):
    product_name = forms.CharField(required=False, label='Product Name')
    min_price = forms.DecimalField(required=False, label='Min Price', decimal_places=2, max_digits=10)
    max_price = forms.DecimalField(required=False, label='Max Price', decimal_places=2, max_digits=10)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label='Category')


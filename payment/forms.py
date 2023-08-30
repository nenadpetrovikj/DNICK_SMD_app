from django import forms
from django_countries.fields import CountryField

from account.models import UserBase


class PaymentForm(forms.ModelForm):

    # Personal Info
    email = forms.EmailField(
        label='Email', max_length=100, help_text='Required', widget=forms.TextInput(
            attrs={'class': 'form-control', 'id': 'email'}))
    
    first_name = forms.CharField(
        label='First name', min_length=4, max_length=50, help_text='Required', widget=forms.TextInput(
            attrs={'class': 'form-control', 'id': 'firstname'}))
    
    last_name = forms.CharField(
        label='Last name', min_length=4, max_length=50, help_text='Required', widget=forms.TextInput(
            attrs={'class': 'form-control', 'id': 'lastname'}))
    
    # Delivery details
    phone_number = forms.CharField(
        label='Phone Number', min_length=3, max_length=30, help_text='Required', widget=forms.TextInput(
            attrs={'class': 'form-control', 'id': 'phone-number', 'type': 'tel'}))
    
    country = CountryField()
    
    city = forms.CharField(
        label='City', min_length=1, max_length=150, help_text='Required', widget=forms.TextInput(
            attrs={'class': 'form-control', 'id': 'city'}))
    
    postcode = forms.CharField(
        label='Postal code', min_length=2, max_length=12, help_text='Required', widget=forms.TextInput(
            attrs={'class': 'form-control', 'id': 'postcode'}))
    
    address_line_1 = forms.CharField(
        label='Address Line 1', max_length=150, help_text='Required', widget=forms.TextInput(
            attrs={'class': 'form-control', 'id': 'address1'}))
    
    address_line_2 = forms.CharField(
        label='Address Line 2', max_length=150, help_text='Required', widget=forms.TextInput(
            attrs={'class': 'form-control', 'id': 'address2'}))

    class Meta:
        model = UserBase
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'country', 'city', 'postcode', 'address_line_1', 'address_line_2')
    
    # Checks that are NOT included:
    # - Whether the city is legit, meaning whether it belongs to the country or not
    # - Whether the phone number is legit, meaning whether it belongs to the user or not
    # - Whether the postcode is legit...

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'].widget.attrs.update({
            'class': 'form-select form-control',
            'id': 'country'
        })
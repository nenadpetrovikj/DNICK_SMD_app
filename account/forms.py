from django import forms
from django_countries.fields import CountryField
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm, SetPasswordForm)

from .models import UserBase


class UserLoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control mb-3',
            'placeholder': 'Enter your username',
            'id': 'login-username',
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'id': 'login-pwd',
        }
    ))

class RegistrationForm(forms.ModelForm):

    # The messages written under error_messages do not appear, if the user does not satisfy the requirements.
    # The browser does not let the user send the post data to the server, if these requirements are not satisfied.
    username = forms.CharField(label='Username', min_length=4, max_length=50, help_text='Required', 
                               error_messages={'required': 'Please enter a username.',
                                               'min_length': 'Username has to be more than 4 characters long.',
                                               'max_length': 'Username has to be less than 50 characters long.'})
    email = forms.EmailField(label='Email', max_length=100, help_text='Required',
                             error_messages={'required': 'Please enter an email.',
                                             'invalid': 'Please enter a valid email address.',
                                             'max_length': 'Email has to be less than 100 characters long.'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput, help_text='At least 8 characters and 1 digit',
                               error_messages={'required': 'Please enter a password.'})
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput, help_text='Required',
                               error_messages={'required': 'Please enter the password again.'})

    class Meta:
        model = UserBase
        fields = ('username', 'email',)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = UserBase.objects.filter(username=username)
        if r.count():
            raise forms.ValidationError("Username already exists.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already taken.")
        return email
    
    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8 or not any(char.isdigit() for char in password):
            raise forms.ValidationError("Password must have at least 8 characters and 1 digit.")
        return password
    
    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data['password2']
        if password == None:
            return
        if password != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Enter a username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Enter a valid email address'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Enter a valid password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Confirm the entered password'})

class UserEditForm(forms.ModelForm):

    # Personal Info
    username = forms.CharField(
        label='Username', help_text='Cannot Be Changed Later', widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'id': 'form-username', 'readonly': 'readonly'}))
    
    email = forms.EmailField(
        label='Email', max_length=100, help_text='Required', widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter an email', 'id': 'form-email'}))

    first_name = forms.CharField(
        label='First name', min_length=4, max_length=50, required=False, help_text='Optional', widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Enter your first name', 'id': 'form-firstname'}))
    
    last_name = forms.CharField(
        label='Last name', min_length=4, max_length=50, required=False, help_text='Optional', widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Enter your last name', 'id': 'form-lastname'}))
    
    # Delivery details
    phone_number = forms.CharField(
        label='Phone Number', min_length=3, max_length=30, required=False, help_text='Optional', widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Enter your phone number', 'id': 'form-phone', 'type': 'tel'}))
    
    country = CountryField(blank=True, help_text='Optional')
    
    city = forms.CharField(
        label='City', min_length=1, max_length=150, required=False, help_text='Optional', widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Enter the city you live in', 'id': 'form-city'}))
    
    postcode = forms.CharField(
        label='Postal code', min_length=2, max_length=12, required=False, help_text='Optional', widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Enter your postal code', 'id': 'form-postcode'}))
    
    address_line_1 = forms.CharField(
        label='Address Line 1', max_length=150, required=False, help_text='Optional', widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Enter your street name and civic number', 'id': 'form-address1'}))
    
    address_line_2 = forms.CharField(
        label='Address Line 2', max_length=150, required=False, help_text='Optional', widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Enter your apartment number', 'id': 'form-address2'}))

    class Meta:
        model = UserBase
        fields = ('email', 'username', 'first_name', 'last_name', 'phone_number',
                  'country', 'city', 'postcode', 'address_line_1', 'address_line_2')
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if UserBase.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("The email you have entered is already taken.")
        return email
    
    # Checks that are NOT included:
    # - Whether the city is legit, meaning whether it belongs to the country or not
    # - Whether the phone number is legit, meaning whether it belongs to the user or not
    # - Whether the postcode is legit...

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'].widget.attrs.update({
            'class': 'form-select form-control mb-3',
            'id': 'form-country'
        })

class PwdResetForm(PasswordResetForm):

    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Enter your email address', 'id': 'form-email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        u = UserBase.objects.filter(email=email)
        if not u:
            raise forms.ValidationError('No account is associated with this email address.')
        return email

class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Enter the new password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Repeat the new password', 'id': 'form-new-pass2'}))
    
    # More checks for the new password can be added
    def clean_new_password1(self):
        new_password1 = self.cleaned_data['new_password1']
        if new_password1.isdigit():
            raise forms.ValidationError("Password can not be entirely numeric.")
        if len(new_password1) < 8 or not any(char.isdigit() for char in new_password1):
            raise forms.ValidationError("Password must have at least 8 characters and 1 digit.")
        return new_password1
    
    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data['new_password2']
        if new_password1 == None:
            return
        if new_password1 != new_password2:
            raise forms.ValidationError("Passwords do not match.")
        return new_password2
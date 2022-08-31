from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import Account
from blood_donation_app.models import *

class RegistrationForm(UserCreationForm):

    email = forms.EmailField(max_length=100, help_text="Required, Enter a valid email address!")

    class Meta:
        model = Account
        fields = ("name", "phone", "blood_group", "state", "city", "email", "password1", "password2", "donate_plasma")

    # -------------------

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()

        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['city'].queryset = City.objects.filter(state_id=state_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.state.city_set.order_by('name')

    # -------------------

class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'id': 'loginPassword', 'autocomplete': 'off'}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'id': 'loginEmail', 'autocomplete': 'off'}))

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        if not authenticate(email=email, password=password):
            raise forms.ValidationError("Invalid Login")

class UserUpdateForm(forms.ModelForm):

    plasma_choices = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )

    phone = forms.CharField(label="Phone Number", widget=forms.NumberInput(attrs={'id': 'dashboardPhone'}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'id': 'dashboardEmail'}))
    donate_plasma = forms.ChoiceField(label="Donate Plasma", choices=plasma_choices, widget=forms.Select(attrs={'id': 'dashboardPlasma'}))

    # -------------------

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()

        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['city'].queryset = City.objects.filter(state_id=state_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.state.city_set.order_by('name')

    # -------------------
    
    class Meta:
        model = Account
        fields = ["email", "phone", "state", "city", "donate_plasma"]

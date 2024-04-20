from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Customer, Contractor
from django.forms import ModelForm, TextInput, EmailInput, Textarea
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomerProfileForm(ModelForm):
    phone_number = PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={
        'class': 'form-control',
        'placeholder': 'Введите номер телефона'
    }))

    class Meta:
        model = Customer
        fields = ['name', 'surname', 'email', 'phone_number']
        widgets = {
            "name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя'
            }),
            "surname": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите фамилию'
            }),
            "email": EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите почту'
            })
        }


class ContractorProfileForm(ModelForm):
    phone_number = PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={
        'class': 'form-control',
        'placeholder': 'Введите номер телефона'
    }))

    class Meta:
        model = Contractor
        fields = ['name', 'surname', 'experience', 'email', 'phone_number']
        widgets = {
            "name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя'
            }),
            "surname": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите фамилию'
            }),
            "experience": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Напишите опыт ваших предыдущих проектов'
            }),

            "email": EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите почту'
            })
        }


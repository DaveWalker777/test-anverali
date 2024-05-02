from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField('Имя', max_length=50)
    surname = models.CharField('Фамилия', max_length=50)
    email = models.EmailField('Почта')
    phone_number = PhoneNumberField(null=True)

    def __str__(self):
        return self.surname

    class Meta:
        verbose_name = 'Заказчик'
        verbose_name_plural = 'Заказчики'


class Contractor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField('Имя', max_length=50)
    surname = models.CharField('Фамилия', max_length=50)
    experience = models.TextField('Опыт работы и проекты')
    email = models.EmailField('Почта')
    phone_number = PhoneNumberField(null=True)

    def __str__(self):
        return self.surname

    class Meta:
        verbose_name = 'Исполнитель'
        verbose_name_plural = 'Исполнители'

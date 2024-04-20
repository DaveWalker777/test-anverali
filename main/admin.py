from django.contrib import admin
from .models import Contractor, Customer, CustomerFormStatus, ContractorFormStatus

admin.site.register(Contractor)
admin.site.register(Customer)


class CustomerFormStatusAdmin(admin.ModelAdmin):
    list_display = ('user', 'form_submitted')


class ContractorFormStatusAdmin(admin.ModelAdmin):
    list_display = ('user', 'form_submitted')


admin.site.register(CustomerFormStatus, CustomerFormStatusAdmin)
admin.site.register(ContractorFormStatus, ContractorFormStatusAdmin)
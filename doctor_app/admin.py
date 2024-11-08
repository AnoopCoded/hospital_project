from django.contrib import admin
from doctor_app.models import *
# Register your models here.
class PatientBillAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor_name', 'total', 'amount_due', 'paid']
    search_fields = ['patient__name', 'doctor_name']

admin.site.register(PatientBill, PatientBillAdmin)
admin.site.register(Insurance)
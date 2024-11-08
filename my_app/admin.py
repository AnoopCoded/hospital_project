from django.contrib import admin
from .models import *
from doctor_app.models import *

# Register your models here.
admin.site.register(doctorDetails)

admin.site.register(Department)
admin.site.register(Patient)
admin.site.register(HealthTip)
admin.site.register(EducationalMaterial)
admin.site.register(Resource)

admin.site.register(Appointment)
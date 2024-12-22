from django.contrib import admin
from .models import CustomUser, Appointment, ServiceType, AppointmentServiceType, Examination, Patient, Payment

admin.site.register(CustomUser)
admin.site.register(Appointment)
admin.site.register(ServiceType)
admin.site.register(AppointmentServiceType)
admin.site.register(Examination)
admin.site.register(Patient)
admin.site.register(Payment)
# Register your models here.

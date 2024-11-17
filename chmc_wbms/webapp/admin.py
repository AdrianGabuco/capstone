from django.contrib import admin
from .models import CustomUser, Appointment, ServiceType, AppointmentServiceType

admin.site.register(CustomUser)
admin.site.register(Appointment)
admin.site.register(ServiceType)
admin.site.register(AppointmentServiceType)
# Register your models here.

from django.contrib import admin
from .models import CustomUser, Appointment, ServiceType, AppointmentServiceType, Examination, Patient, Payment


class ExaminationAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'attending_doctor', 'date_created', 'get_unique_code', 'get_raw_unique_code')
    readonly_fields = ('get_unique_code', 'get_raw_unique_code')
    search_fields = ('get_unique_code', 'get_raw_unique_code')

    def get_unique_code(self, obj):
        return obj.get_unique_code()
    get_unique_code.short_description = "Unique Code"

    def get_raw_unique_code(self, obj):
        return obj.get_raw_unique_code()
    get_raw_unique_code.short_description = "Raw SHA-256 Code"
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Appointment)
admin.site.register(ServiceType)
admin.site.register(AppointmentServiceType)
admin.site.register(Examination, ExaminationAdmin)
admin.site.register(Patient)
admin.site.register(Payment)
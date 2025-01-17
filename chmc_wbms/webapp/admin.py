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

class PatientAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 
        'last_name', 
        'get_formatted_id', 
        'get_string_to_hash', 
        'get_secure_hashed_id'
    )
    readonly_fields = ('get_formatted_id', 'get_string_to_hash', 'get_secure_hashed_id')

    def get_formatted_id(self, obj):
        """Display the formatted ID in the admin."""
        return obj.get_formatted_id()
    get_formatted_id.short_description = "Formatted ID"

    def get_string_to_hash(self, obj):
        """Display the string used for hashing."""
        salt = "Patient2025"
        pepper = "Identity2024"
        formatted_id = obj.get_formatted_id()
        return f"{salt}{formatted_id}{pepper}"
    get_string_to_hash.short_description = "String to Hash"

    def get_secure_hashed_id(self, obj):
        """Display the hashed ID (Raw SHA-256 Code)."""
        return obj.get_secure_hashed_id()
    get_secure_hashed_id.short_description = "Raw SHA-256 Code"


admin.site.register(CustomUser)
admin.site.register(Appointment)
admin.site.register(ServiceType)
admin.site.register(AppointmentServiceType)
admin.site.register(Examination, ExaminationAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Payment)
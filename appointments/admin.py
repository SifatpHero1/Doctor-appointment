from django.contrib import admin
from .models import Doctor, Appointment

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'email', 'phone', 'available_days')
    search_fields = ('name', 'specialization')
    list_filter = ('specialization',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'time', 'status')
    search_fields = ('patient__username', 'doctor__name')
    list_filter = ('status', 'date', 'doctor')


from django.contrib import admin
from .models import PatientHistory, PatientFile


@admin.register(PatientFile)
class PatientFielAdmin(admin.ModelAdmin):
    pass

@admin.register(PatientHistory)
class PatientHitoryAdmin(admin.ModelAdmin):
    pass
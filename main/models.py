from typing import Iterable, Optional
from django.db import models
from .helpers import UploadTo


class PatientHistory(models.Model):
    patient = models.OneToOneField('accounts.User', on_delete=models.SET_NULL, null=True, related_name="patient")
    doctor = models.ManyToManyField('accounts.User', related_name="doctor")
    patient_name = models.CharField(max_length=256)
    patient_birth_date = models.DateField(help_text='Patient birth date')
    patient_med_condition = models.TextField()

    # def __str__(self):
    #     return self.patient or "None"


class PatientFile(models.Model):
    file = models.FileField(upload_to=UploadTo("patients"))
    patient_history = models.ForeignKey(PatientHistory, on_delete=models.CASCADE, related_name='patient_history')


import django_filters
from django.db import models as django_models
from django_filters import rest_framework as filters

from .models import PatientHistory

class PatientHistoryFilter(filters.FilterSet):
    class Meta:
        model = PatientHistory
        fields = {
            'patient_birth_date': ('lte', 'gte')
        }

    filter_overrides = {
        django_models.DateTimeField: {
            'filter_class': django_filters.IsoDateTimeFilter
        },
    }
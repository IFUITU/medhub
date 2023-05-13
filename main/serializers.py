from rest_framework import serializers
from rest_framework.validators import ValidationError

from .models import PatientHistory, PatientFile
from django.conf import settings

class PatientFileCreateSerializer(serializers.ModelSerializer):
    file = serializers.ListField(
        child = serializers.FileField(max_length = 1000000, allow_empty_file = False, use_url = False),
        write_only = True, required = True
    )

    class Meta:
        model = PatientFile
        fields = "__all__"
        extra_kwargs = {"id":{"read_only":True},}

    def create(self, validated_data): #save multiple files in one request
        patient_history=validated_data['patient_history']
        files=validated_data.pop('file')
        patient_file=None
        for file in files:
            patient_file=PatientFile.objects.create(file=file, patient_history=patient_history)
        return validated_data

    def validate_file(self, values): #validate max upload size
        total_size = 0
        for file in values:
            total_size += file.size
        if total_size > int(settings.MAX_UPLOAD_SIZE):
            raise ValidationError("Maximum file size must be 5MB!")
        return values

    def save(self, **kwargs):
        pass

class PatientFileSerializer(serializers.ModelSerializer):        
    class Meta:
        model = PatientFile
        fields = '__all__'


class PatientHistorySerializer(serializers.ModelSerializer):
    uploaded_files = serializers.ListField(
        child = serializers.FileField(max_length = 1000000, allow_empty_file = False, use_url = False),
        write_only = True, required = False
    )

    class Meta:
        model = PatientHistory
        fields = (
            'id',
            'patient_name',
            'patient_birth_date', 
            'patient', 
            'doctor', 
            'patient_med_condition', 
            'uploaded_files',)
        extra_kwargs = {
            "id":{"read_only":True},}

    def create(self, validated_data): #to set mtm field & save multiple files in one request.
        instance = None
        doctor_ids = validated_data.pop("doctor", None)
        patient_files = validated_data.pop('uploaded_files', None)
        instance = PatientHistory.objects.create(**validated_data)
        if doctor_ids:
            instance.doctor.set(doctor_ids)

        if patient_files: #create PatientHistory with multiple files in one request
            for file in  patient_files:
                PatientFile.objects.create(file=file, patient_history=instance)

        return instance


class GroupedPatientInfoSerializer(serializers.Serializer):
    patient_history = PatientHistorySerializer()
    patient_files = PatientFileSerializer(many=True)

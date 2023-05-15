import tempfile
from rest_framework.test import APITestCase
from rest_framework import status

from .models import PatientFile, PatientHistory
from accounts.models import User

from django.contrib.auth.hashers import make_password
from PIL import Image
from django.core.files.base import File
from datetime import datetime


HOST = "http://127.0.0.1:8000/api"


class PatientHistoryTest(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create(
            username='test_user', 
            password=make_password('123'),
            # user_type=""
            )

        self.patient_1 = User.objects.create(
            username='patient_1', 
            password=make_password('123'),
            user_type="2"
            )

        self.patient_2 = User.objects.create(
            username='patient_2', 
            password=make_password('123'),
            user_type="2"
            )
        
        self.patient_3 = User.objects.create(
            username='patient_3', 
            password=make_password('123'),
            user_type="2"
            )

        self.doctor_1 = User.objects.create(
            username='doctor_1', 
            password=make_password('123'),
            user_type="1"
            )

        self.doctor_2 = User.objects.create(
            username='doctor_2', 
            password=make_password('123'),
            user_type="1"
            )

        self.doctor_3 = User.objects.create(
            username='doctor_3', 
            password=make_password('123'),
            user_type="1"
            )
        
        #"ph" is "patient history"
        self.ph_1 = PatientHistory.objects.create(
            patient_name="patient_1",
            patient_birth_date="2000-05-06",
            patient=self.patient_1,
            patient_med_condition="Med condition of patient_1 is good!",
        )
        self.ph_1.doctor.add(self.doctor_1, self.doctor_2, self.doctor_3)

        #pf is "patient file"
        self.pf_1 = PatientFile.objects.create(
            patient_history=self.ph_1,
            file=File(self.make_image_file()),
        )


    def activate_credentials(self, username, password):
        res = self.client.post('http://127.0.0.1:8000/user/log/', {
            'username':username,
            'password':password}, format='json')
        self.access_token = None
        if res.status_code == 200:
            self.access_token = res.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.access_token}')
    
    def make_image_file(self):
        """to create fake testing file"""
        image = Image.new('RGB', (100, 100))

        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        tmp_file.seek(0)
        return tmp_file


    def test_history_as_patient_user(self):
        self.activate_credentials('patient_1', '123')

        #access to patient history as patient user
        res = self.client.get(f"{HOST}/patient-history/", format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        #UPDATE
        res = self.client.patch(f"{HOST}/patient-history/{self.ph_1.id}/", 
                                {"patient_name":"patient_name"}, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        #delete
        res = self.client.delete(f"{HOST}/patient-history/{self.ph_1.id}/", format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


    def test_history_as_doctor_user(self):
        """Only doctors who worked with patient 
        can touch patients' history data, other doctors can't"""
        self.activate_credentials('doctor_1', '123')
        
        #create new history with multiple files 
        res = self.client.post(f"{HOST}/patient-history/", 
            { 
                'patient_name':"patient_2",
                'patient_birth_date':"2000-05-06",
                'patient':self.patient_2.id,
                'doctor':[self.doctor_1.id, self.doctor_3.id],
                'uploaded_files':[self.make_image_file(), self.make_image_file()],
                'patient_med_condition':"Med condition of patient_1 is good!",
            }, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        #access history as doctor user
        res = self.client.get(f"{HOST}/patient-history/", format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        #update history as doctor
        res = self.client.patch(f"{HOST}/patient-history/{self.ph_1.id}/", 
                                {"patient_name":"patient_name"}, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        #delete patient_history
        res = self.client.delete(f"{HOST}/patient-history/{self.ph_1.id}/", format="json")
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_files_as_doctor(self):
        """Only doctors who worked with patient 
        can touch patients' files data, other doctors can't"""

        self.activate_credentials('doctor_2', '123')
        
        #create new multiple file
        res = self.client.post(f"{HOST}/patient-file/", 
            {
                'patient_history': self.ph_1.id,
                'file':[self.make_image_file()],
            }, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        #access file as doctor user
        res = self.client.get(f"{HOST}/patient-file/{self.pf_1.id}/", format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        #update file as doctor
        res = self.client.patch(f"{HOST}/patient-file/{self.ph_1.id}/", 
            {
                'file':[self.make_image_file()],
            }, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        #delete file
        res = self.client.delete(f"{HOST}/patient-file/{self.ph_1.id}/", format="json")
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_filters_as_doctor(self):
        search_val = "name" #search via name, birth_date, med_condition
        filter_val = {
            'patient_name':'name',
            'patient_birth_date':"2001-06-08",
            'patient_med_con':"Good enought."
        }
        self.activate_credentials('doctor_3', '123')

        res = self.client.get(f"{HOST}/patient-history-filter/?search={search_val}", format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        res = self.client.get(f'{HOST}/patient-history-filter/?patient_name={filter_val["patient_name"]}&patient_birth_date={filter_val["patient_birth_date"]}&patient_med_condition={filter_val["patient_med_con"]}')
        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_filters_as_ordinary_user(self):
        search_val = "name" #search via name, birth_date, med_condition
        filter_val = {
            'patient_name':'name',
            'patient_birth_date':"2001-06-08",
            'patient_med_con':"Good enought."
        }
        self.activate_credentials('patient_1', '123')

        res = self.client.get(f"{HOST}/patient-history-filter/?search={search_val}", format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        res = self.client.get(f'{HOST}/patient-history-filter/?patient_name={filter_val["patient_name"]}&patient_birth_date={filter_val["patient_birth_date"]}&patient_med_condition={filter_val["patient_med_con"]}')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

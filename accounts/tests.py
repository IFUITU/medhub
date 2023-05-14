from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth.hashers import make_password

from .models import User


HOSTNAME = 'http://127.0.0.1:8000/user'


class AccountsTest(APITestCase):
    def setUp(self):

        self.test_user = User.objects.create(
            username='test_user', 
            password=make_password('123'),
            # user_type=""
            )

        self.patient_1 = User.objects.create(
            username='patinet_1', 
            password=make_password('123'),
            user_type="2"
            )

        self.patient_2 = User.objects.create(
            username='patient_2', 
            password=make_password('123'),
            user_type="2"
            )

        self.doctor_1 = User.objects.create(
            username='docotr_1', 
            password=make_password('123'),
            user_type="1"
            )

        self.doctor_2 = User.objects.create(
            username='doctor_2', 
            password=make_password('123'),
            user_type="1"
            )
    
    def activate_credentials(self, username, password):
        res = self.client.post(f'{HOSTNAME}/log/', {
            'username':username,
            'password':password}, format='json')
        self.access_token = None
        if res.status_code == 200:
            self.access_token = res.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.access_token}')


    def test_login(self):
        #existance user
        res = self.client.post(f'{HOSTNAME}/log/', 
            {'username':"test_user",
             'password':'123'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        #wrong user
        res = self.client.post(f'{HOSTNAME}/log/', 
            {'username':"test",
             'password':'123'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout(self):
        self.activate_credentials('test_user', '123')
        res = self.client.delete(f'{HOSTNAME}/log/', format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
  
    def test_profile(self):
        #real user 
        self.activate_credentials('test_user', '123')
        res = self.client.get(f'{HOSTNAME}/{self.test_user.id}/', format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        #real user Update itself
        res = self.client.patch(f'{HOSTNAME}/{self.test_user.id}/', 
                              {"user_type":"1"}, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['user_type'], "1")

        #real user Delete itself
        res = self.client.delete(f'{HOSTNAME}/{self.test_user.id}/', format='json')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        #other user cant touch others' info
        self.activate_credentials('patient_1', '123') #authorized as "patient_1"
        res = self.client.get(f'{HOSTNAME}/{self.test_user.id}/', format='json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        #OTHER user can't update others info
        res = self.client.patch(f'{HOSTNAME}/{self.test_user.id}/', 
                              {"user_type":"1"}, format='json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        
        #OTHER USER CANT DELETE OTHERS
        res = self.client.delete(f'{HOSTNAME}/{self.test_user.id}/', format='json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        #wrong user 
        self.activate_credentials('test', '123')
        res = self.client.get(f'{HOSTNAME}/5/', format='json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_change_password(self):
        self.activate_credentials('test_user', '123')

        #if you did confirmation errors 
        res = self.client.patch(f'{HOSTNAME}/change-my-pass/', 
                                {'password':"123", "new":"123456", "confirm":"123456@"}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
        #if you endtered wrong password
        res = self.client.patch(f'{HOSTNAME}/change-my-pass/', 
                                {'password':"wrong_password123", "new":"123456", "confirm":"123456"}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
        #if you enter new password less than 6 characters
        res = self.client.patch(f'{HOSTNAME}/change-my-pass/', 
                                {'password':"123", "new":"12345", "confirm":"12345"}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        #if everything is ok
        res = self.client.patch(f'{HOSTNAME}/change-my-pass/', 
                                {'password':"123", "new":"123456", "confirm":"123456"}, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        
from django.db import models
from django.contrib.auth.models import AbstractUser

user_type = (
    ('1', 'doctor'),
    ("2", 'patient'),
)


class User(AbstractUser):
    user_type = models.CharField(max_length=1, choices=user_type)



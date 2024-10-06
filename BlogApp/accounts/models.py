from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class CustomeUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = ['email']


    def __str__(self):
        return self.username
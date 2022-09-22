import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    activation_token = models.UUIDField(default=uuid.uuid4)

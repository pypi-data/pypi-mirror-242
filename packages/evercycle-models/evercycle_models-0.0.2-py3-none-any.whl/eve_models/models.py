from django.db import models


class Organization(models.Models):
    name = models.CharField(max_length=50)
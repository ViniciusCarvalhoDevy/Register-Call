from django.db import models

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=255)
    document = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name
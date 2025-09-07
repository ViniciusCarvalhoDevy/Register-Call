from django.db import models

# Create your models here.
class Demand(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return  self.name + " - " + self.description
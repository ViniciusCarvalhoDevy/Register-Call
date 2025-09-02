from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CustomerUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)

class CallRegister(models.Model):
    collaborator = models.CharField(max_length=255)
    dateCall = models.DateField()
    user = models.ForeignKey('CustomerUser.CustomerUser', on_delete=models.CASCADE)
    company = models.ForeignKey('Company.Company', on_delete=models.CASCADE)
    demand = models.ForeignKey('Demand.Demand', on_delete=models.CASCADE)
    observation = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.customer_name} - {self.company.name} - {self.demand.name}"
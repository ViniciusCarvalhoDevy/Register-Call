from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CustomerUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return self.user.username

class CallRegister(models.Model):
    collaborator = models.CharField(max_length=255)
    dateCall = models.DateField()
    user = models.ForeignKey('CustomerUser.CustomerUser', on_delete=models.PROTECT)
    company = models.ForeignKey('Company.Company', on_delete=models.PROTECT)
    demand = models.ForeignKey('Demand.Demand', on_delete=models.PROTECT)
    observation = models.TextField(blank=True, null=True)
    value = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    

    def __str__(self):
        return f"{self.collaborator} - {self.company.name} - {self.demand.description}"
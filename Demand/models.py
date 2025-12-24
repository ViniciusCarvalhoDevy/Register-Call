from django.db import models

# Create your models here.
class Demand(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=False, default='')
    user = models.ForeignKey('CustomerUser.CustomerUser', on_delete=models.PROTECT, related_name='demand_has_user')
    
    def __str__(self):
        return  self.name + " - " + self.description
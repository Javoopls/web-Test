from django.db import models

# Create your models here.
class Payment(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name="id")
    amount = models.IntegerField(verbose_name="amount")
    account = models.CharField(max_length=200, verbose_name="account")
    created_at = models.DateTimeField(auto_now_add=True)  
    description = models.CharField(max_length=200,verbose_name="description")
    method = models.CharField(max_length=200,verbose_name="method")
    status = models.CharField(max_length=200,verbose_name="status")
    type = models.CharField(max_length=200,verbose_name="type")
    link = models.CharField(max_length=200,verbose_name="link")
    
    def __str__(self):
        return self.nombreRegion
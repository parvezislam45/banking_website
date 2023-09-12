from django.db import models
from django.contrib.auth.models import User
from .constants import ACCOUNT_TYPE,GENDER

# Create your models here.

class userBankAccounts(models.Model):
    user = models.OneToOneField(User,related_name='account',on_delete=models.CASCADE)
    accountType = models.CharField(max_length=50,choices=ACCOUNT_TYPE)
    account_no = models.IntegerField(unique=True)
    date_of_Birth = models.DateField(null=True,blank=True)
    gender = models.CharField(max_length=100,choices=GENDER)
    initial_deposit_date = models.DateField(auto_now_add=True)
    balance = models.DecimalField(default=0,max_digits=12,decimal_places=2)
    
    
    def __str__(self) :
         return str(self.account_no)
    
class userAddress(models.Model):
     user = models.OneToOneField(User,related_name='address',on_delete=models.CASCADE)
     street_address = models.CharField(max_length=100)
     city = models.CharField(max_length=100)
     postal_code = models.IntegerField()
     country = models.CharField(max_length=100)
     
     
     def __str__(self) :
         return str(self.user.email)
    
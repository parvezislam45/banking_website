from django.db import models
from accounts.models import userBankAccounts
from .constants import TRANSACTION_TYPE
# Create your models here.
class Transactions(models.Model):
    account = models.ForeignKey(userBankAccounts,related_name='transactions',on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2,max_digits=12)
    balance_after_transaction = models.DecimalField(decimal_places=2,max_digits=12)
    transactions_type = models.IntegerField(choices=TRANSACTION_TYPE,null=True)
    times = models.DateTimeField(auto_now_add=True)
    loan_approve = models.BooleanField(default=False)
    
    class Meta:
        ordering =['times']
        
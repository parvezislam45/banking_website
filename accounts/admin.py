from django.contrib import admin
from .models import userBankAccounts,userAddress

# Register your models here.
admin.site.register(userBankAccounts)
admin.site.register(userAddress)


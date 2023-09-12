from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .constants import ACCOUNT_TYPE,GENDER
from .models import userBankAccounts,userAddress


class userRegisterForm(UserCreationForm):
     gender = forms.ChoiceField(choices=GENDER) 
     street_address = forms.CharField(max_length=100)
     city = forms.CharField(max_length=100)
     postal_code = forms.IntegerField()
     country = forms.CharField(max_length=100)
     
     
     
     class Meta:
        model = User
        fields = ['username','email','password1','password2','first_name','last_name',
                  'gender','postal_code','country','street_address',
                  'city',
                  ]
     def save(self,commit=True):
        our_user = super().save(commit=False)
        if commit == True :
           our_user.save()
           gender = self.cleaned_data.get('gender')
           street_address = self.cleaned_data.get('street_address')
           city = self.cleaned_data.get('city')
           postal_code = self.cleaned_data.get('postal_code')
           country = self.cleaned_data.get('country')
           
           
           
           userAddress.objects.create(
              user = our_user,
              street_address= street_address,
              postal_code = postal_code,
              city = city,
              country = country,            
              
           )
           
           userBankAccounts.objects.create(
              user = our_user,
              gender = gender,
              
           )
           return our_user
        
     def __init__(self,*args, **kwargs):
           super().__init__(*args, **kwargs)
           
           for field in self.fields:
              self.fields[field].widget.attrs.update({
                 'class' : (
                    'block w-full p-2 mt-2 text-gray-700 bg-gray-200 appearance-none focus:outline-none focus:bg-gray-300 focus:shadow-inner'
                 )
              })
        

           
   
     
     
    

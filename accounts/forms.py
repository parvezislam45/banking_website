from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .constants import ACCOUNT_TYPE,GENDER
from .models import userBankAccounts,userAddress
from .models import userBankAccounts,userAddress


class userRegisterForm(UserCreationForm):
     accountType = forms.ChoiceField(choices=ACCOUNT_TYPE)
     date_of_Birth = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
     gender = forms.ChoiceField(choices=GENDER) 
     street_address = forms.CharField(max_length=100)
     city = forms.CharField(max_length=100)
     postal_code = forms.IntegerField()
     country = forms.CharField(max_length=100)
     
     
     
     class Meta:
        model = User
        fields = ['username','email','password1','password2','first_name','last_name',
                  'gender','postal_code','country','street_address',
                  'city','accountType','date_of_Birth'
                  ]
     def save(self,commit=True):
        our_user = super().save(commit=False)
        if commit == True :
           our_user.save()
           accountType = self.cleaned_data.get('accountType')
           date_of_Birth = self.cleaned_data.get('date_of_Birth')
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
              accountType = accountType,
              date_of_Birth = date_of_Birth,
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
              
              
              
              
class UserUpdateForm(forms.ModelForm):
     accountType = forms.ChoiceField(choices=ACCOUNT_TYPE)
     date_of_Birth = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
     gender = forms.ChoiceField(choices=GENDER) 
     street_address = forms.CharField(max_length=100)
     city = forms.CharField(max_length=100)
     postal_code = forms.IntegerField()
     country = forms.CharField(max_length=100)
     
     class Meta:
        model = User
        fields = ['first_name','last_name','email','username']
     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'block w-full p-2 mt-2 text-gray-700 bg-gray-200 appearance-none focus:outline-none focus:bg-gray-300 focus:shadow-inner'
                )
            })
            
        if self.instance:
            try:
                user_account = self.instance.account
                user_address = self.instance.address
            except userBankAccounts.DoesNotExist:
                user_account = None
                user_address = None

            if user_account:
                self.fields['accountType'].initial = user_account.accountType
                self.fields['gender'].initial = user_account.gender
                self.fields['date_of_Birth'].initial = user_account.date_of_Birth
                self.fields['street_address'].initial = user_address.street_address
                self.fields['city'].initial = user_address.city
                self.fields['postal_code'].initial = user_address.postal_code
                self.fields['country'].initial = user_address.country
                
     def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

            user_account, created = userBankAccounts.objects.get_or_create(user=user) # jodi account thake taile seta jabe user_account ar jodi account na thake taile create hobe ar seta created er moddhe jabe
            user_address, created = userAddress.objects.get_or_create(user=user) 

            user_account.accountType = self.cleaned_data['accountType']
            user_account.gender = self.cleaned_data['gender']
            user_account.date_of_Birth = self.cleaned_data['date_of_Birth']
            user_account.save()

            user_address.street_address = self.cleaned_data['street_address']
            user_address.city = self.cleaned_data['city']
            user_address.postal_code = self.cleaned_data['postal_code']
            user_address.country = self.cleaned_data['country']
            user_address.save()

        return user
        

           
   
     
     
    

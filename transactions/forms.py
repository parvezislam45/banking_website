from django import forms
from .models import Transactions


class TransactionsForm(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = ['amount','transactions_type']
        
    def __init__(self,*args, **kwargs):
        self.account = kwargs.pop('account')
        super().__init__(*args, **kwargs)
        self.fields['transactions_type'].disabled = True
        self.fields['transactions_type'].widget = forms.HiddenInput()
        
    def save(self,commit=True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance
        return super().save()
        
class DepositForm(TransactionsForm):
    def clean_amount(self):
        min_deposit_amount = 100
        amount = self.cleaned_data.get('amount')
        if amount < min_deposit_amount:
            raise forms.ValidationError(f'You need to Deposit at Least {min_deposit_amount} $')
        return amount
    
    
    
class WithdrawalForm(TransactionsForm):
    def clean_amount(self):
        account = self.account
        min_withdraw_amount = 500
        max_withdraw_amount = 20000
        balance = account.balance
        amount = self.cleaned_data.get('amount')
        if amount < min_withdraw_amount:
            raise forms.ValidationError(f'You Can Withdrawal at Least {min_withdraw_amount}')
        if amount > max_withdraw_amount:
            raise forms.ValidationError(f'You Can Withdraw at Mose {max_withdraw_amount}')
        if amount > balance:
            raise forms.ValidationError(f'You Have {balance} $ in your Account.''You can not Withdraw more then your account Balance')
        return amount
    
    
    
class LoanRequestForm(TransactionsForm):
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        
        return amount
    
    

    
        
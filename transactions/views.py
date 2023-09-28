from typing import Any
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import get_object_or_404,redirect
from django.views import View
from django.http import HttpResponse
from django.views.generic import CreateView,ListView,TemplateView
from transactions.constants import DEPOSIT,WITHDRAWAL,LOAN,LOAN_PAID
from transactions.forms import (DepositForm,WithdrawalForm,LoanRequestForm)
from transactions.models import Transactions
from datetime import datetime
from django.db.models import Sum

# Create your views here.

class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name = 'transactionForm.html'
    model = Transactions
    title = ''
    success_url = reverse_lazy('transaction_report')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # template e context data pass kora
        context.update({
            'title': self.title
        })

        return context

    
    
class DepositView(TransactionCreateMixin):
    form_class = DepositForm
    title = 'DEPOSIT'
    def get_initial(self):
        initial = {'transactions_type': DEPOSIT}
        return initial
    
    def form_valid(self,form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        if not account.initial_deposit_date:
            now = timezone.now()
            account.initial_deposit_date = now
        account.balance += amount
        account.save(update_fields =['initial_deposit_date','balance'])
        
        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))} $ was Deposited Your Account Successfully'
        )
        return super().form_valid(form)
    
    
class WithdrawView(TransactionCreateMixin):
    form_class = WithdrawalForm
    title = 'Withdraw Money'
    def get_initial(self):
        initial = {'transactions_type': WITHDRAWAL}
        return initial
    
    def form_valid(self,form):
        amount = form.cleaned_data.get('amount')
        self.request.user.account.balance -= form.cleaned_data.get('amount')
        balance = 300
        self.request.user.account.save(update_fields=['balance'])
        
        messages.success(
            self.request,
            f'SuccessFully Withdrawal{"{:,.2f}".format(float(amount))} $ From Your Account'
        )
        return super().form_valid(form)
    
    
    
class LoanRequestView(TransactionCreateMixin):
    form_class = LoanRequestForm
    title = 'Request For Loan'
    def get_initial(self):
        initial = {'transactions_type': LOAN}
        return initial
    
    def form_valid(self,form):
        amount = form.cleaned_data.get('amount')
        current_loan_count = Transactions.objects.filter(
        account=self.request.user.account,
        transactions_type=3,
        loan_approve=True
        ).count()
        if current_loan_count >= 3 :
            return HttpResponse("You Have Cross The Loan Limit")
        
        messages.success(
            self.request,
            f'Loan Request For{"{:,.2f}".format(float(amount))} $ Submitted SuccessFully'
        )
        return super().form_valid(form)
    
    
class TransactionReportView(LoginRequiredMixin, ListView):
    template_name = 'transactionReport.html'
    model = Transactions
    balance = 0
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(
            account=self.request.user.account
        )
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        
        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            
            queryset = queryset.filter(timestamp__date__gte=start_date, timestamp__date__lte=end_date)
            self.balance = Transactions.objects.filter(
                timestamp__date__gte=start_date, timestamp__date__lte=end_date
            ).aggregate(Sum('amount'))['amount__sum']
        else:
            self.balance = self.request.user.account.balance
       
        return queryset.distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account': self.request.user.account
        })

        return context
       
    
class PayLoanView(LoginRequiredMixin, View):
    def get(self, request, loan_id):
        loan = get_object_or_404(Transactions, id=loan_id)
        print(loan)
        if loan.loan_approve:
            user_account = loan.account
                # Reduce the loan amount from the user's balance
                # 5000, 500 + 5000 = 5500
                # balance = 3000, loan = 5000
            if loan.amount < user_account.balance:
                user_account.balance -= loan.amount
                loan.balance_after_transaction = user_account.balance
                user_account.save()
                loan.loan_approved = True
                loan.transaction_type = LOAN_PAID
                loan.save()
                return redirect('transactions:loan_list')
            else:
                messages.error(
            self.request,
            f'Loan amount is greater than available balance'
        )

        return redirect('loan_list')


class LoanListView(LoginRequiredMixin,ListView):
    model = Transactions
    template_name = 'loanRequest.html'
    context_object_name = 'loans' # loan list ta ei loans context er moddhe thakbe
    
    def get_queryset(self):
        user_account = self.request.user.account
        queryset = Transactions.objects.filter(account=user_account,transaction_type=3)
        print(queryset)
        return queryset
    
    

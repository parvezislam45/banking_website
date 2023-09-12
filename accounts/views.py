from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import FormView
from .forms import userRegisterForm
from django.contrib.auth import login
from django.urls import reverse_lazy

# Create your views here.
class userRegistrationView(FormView):
    template_name = 'registration.html'
    form_class = userRegisterForm
    success_url = reverse_lazy('register')
    
    def form_valid(self,form):
        print(form.cleaned_data)
        user = form.save()
        login(self.request, user)
        print(user)
        return super().form_valid(form)
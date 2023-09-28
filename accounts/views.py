from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import FormView
from .forms import userRegisterForm,UserUpdateForm
from django.contrib.auth import login,logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView,LogoutView
from django.views import View
from django.shortcuts import redirect

# Create your views here.
class register(FormView):
    template_name = 'registration.html'
    form_class = userRegisterForm
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self,form):
        print(form.cleaned_data)
        user = form.save()
        login(self.request, user)
        print(user)
        return super().form_valid(form)
    
    
class Login(LoginView):
    template_name = 'login.html'
    def get_success_url(self):
        return reverse_lazy('home')
    
    
    
class logOut(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')
    
    
    
class update(View):
    template_name = 'profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('update')  # Redirect to the user's profile page
        return render(request, self.template_name, {'form': form})
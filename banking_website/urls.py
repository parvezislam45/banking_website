
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('account/',include('accounts.urls')),
    path('transaction/',include('transactions.urls')),
]

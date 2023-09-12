from django.urls import path
from .views import userRegistrationView
urlpatterns = [
    path('register/',userRegistrationView.as_view(),name='register')
    
]

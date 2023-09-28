from django.urls import path
from .views import register,Login,logOut,update
urlpatterns = [
    path('register/',register.as_view(),name='register'),
    path('login/',Login.as_view(),name='login'),
    path('logout/',logOut.as_view(),name='logout'),
    path('update/',update.as_view(),name='update'),
   
    
]

from email import generator
from django.urls import path
from password_generator import views

urlpatterns = [
    path('',views.generator,name="generator"),
    path('password/', views.generated, name="generated")
    
]
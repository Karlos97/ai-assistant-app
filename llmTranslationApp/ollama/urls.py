from django.urls import path
from . import views

urlpatterns = [
    path('mistral-chat/', views.mistral_chat, name='mistral_chat'),
]

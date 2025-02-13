from django.urls import path
from . import views

urlpatterns = [
    path('ai-model/', views.ai_model, name='ai_model'),
]

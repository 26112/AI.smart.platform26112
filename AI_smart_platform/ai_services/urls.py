from django.urls import path
from .views import run_ai_service

urlpatterns = [
    path('run/', run_ai_service, name='run_ai_service'),
]

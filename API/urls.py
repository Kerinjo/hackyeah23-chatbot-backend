from django.urls import path
from . import views

urlpatterns = [
    path('handle_message/', views.handle_message, name='handle_message'),
]

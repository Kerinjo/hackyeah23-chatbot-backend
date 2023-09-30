from django.urls import path
from . import views

urlpatterns = [
    path('handle_message/', views.handle_message, name='handle_message'),
    path('generate_uuid/', views.generate_uuid, name="generate_uuid"),
    path('fetch_messages/', views.fetch_messages, name="fetch_messages"),
    path('purge/', views.purge, name="purge")
]

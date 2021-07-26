from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'qrcoder'

urlpatterns = [
	path('', qr_view_all, name='qr_view_all'),
]
from django.urls import path, include
from .views import *

urlpatterns = [
    path('load-cities/', load_cities, name="load_cities"),
]
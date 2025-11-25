from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('contact/', contact, name='contact'),
    path('faqs/', faqs, name='faqs'),
    path('ourcompany/', ourcompany, name='ourcompany'),
    path('rates/', rates, name='rates'),
    path('blog/', blog, name='blog'),
    path('teams/', teams, name='teams'),
]
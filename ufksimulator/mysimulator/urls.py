from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('eu-parliament/', views.eu_parliament, name='eu_parliament'),
    path('insert-data/', views.insert_data, name='insert_data'),
    path('check-parliament/', views.check_parliament, name='check_parliament'),
    path('country-parliament/', views.country_parliament, name='country_parliament'),  # Add this line
]

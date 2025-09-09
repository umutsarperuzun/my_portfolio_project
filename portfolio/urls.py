from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.redirect_home),
    path('projects/', views.redirect_home),
    path('contact/', views.redirect_home),
    path('blog/', views.redirect_home),
    path('contact/submit/', views.contact_submit, name='contact_submit'),
]

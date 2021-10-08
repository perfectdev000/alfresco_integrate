from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('cut/<int:pk>/', views.cut, name='cut'),
    path('clear/<int:pk>/', views.clear, name='clear'),
    path('clear-all/', views.clear_all, name='clear_all')
] 
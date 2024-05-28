# market/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('market-list/', views.market_data_list, name='market_data_list'),
    path('market-data/create/', views.market_data_create, name='market_data_create'),
    path('market-data/edit/<int:pk>/', views.market_data_edit, name='market_data_edit'),
    path('market-data/delete/<int:pk>/', views.market_data_delete, name='market_data_delete'),
    path('generate-report/', views.generate_report, name='generate_report'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
]

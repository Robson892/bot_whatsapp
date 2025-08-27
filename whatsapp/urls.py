from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('bots/', views.bot_list, name='bot_list'),
    path('bots/create/', views.bot_create, name='bot_create'),
    path('bots/<int:pk>/', views.bot_detail, name='bot_detail'),
]


from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('', views.home, name='home'),
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    path('login/', auth_views.LoginView.as_view(template_name='whatsapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', views.signup_view, name='signup'),  # <-- rota de cadastro

    path('', views.dashboard, name='dashboard'),
    path('bots/', views.bot_list, name='bot_list'),
    path('bots/create/', views.bot_create, name='bot_create'),
    path('bots/<int:pk>/', views.bot_detail, name='bot_detail'),
    path('bots/<int:pk>/edit/', views.bot_update, name='bot_update'),

]
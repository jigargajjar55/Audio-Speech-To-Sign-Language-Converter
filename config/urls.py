"""A2SL URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from src.core.views import home, auth, animation, dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Home & Information
    path('', home.home_view, name='home'),
    path('about/', home.about_view, name='about'),
    path('contact/', home.contact_view, name='contact'),
    
    # Authentication
    path('login/', auth.login_view, name='login'),
    path('signup/', auth.signup_view, name='signup'),
    path('logout/', auth.logout_view, name='logout'),
    
    # Core Application
    path('animation/', animation.animation_view, name='animation'),
    path('dashboard/', dashboard.dashboard_view, name='dashboard'),
]

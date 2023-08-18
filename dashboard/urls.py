"""
URL configuration for dashboard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from companies import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.signout, name='logout'),
    
    # Companies URLs
    path('companies/data', views.home_data_json, name='companies_data'),
    path('company/<int:company_id>/detail', views.company_data_json, name='company_detail'),
    path('companies/', views.companies, name='companies'),
    path('company_create/', views.company_create, name='company_create'),
    path('company/<int:company_id>', views.company_detail, name='company_detail'),
    path('company/<int:company_id>/delete', views.company_delete, name='company_delete')
]

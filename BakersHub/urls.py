"""BakersHub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from BakersHub import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    # path('<path>/',views.maintenance,name='maintenance'),
    path('premium/',views.premium,name='premium'),
    path('register/',views.register,name='register'),
    path('sign_in/',views.sign_in,name='sign_in'),
    path('forget_password/',views.forget_pass,name='forget_pass'),
    path('logout/', views.log_out, name='logout'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('dashboard/last-month/',views.dashboard_last_month,name='dashboard_last_month'),
    path('dashboard/lifetime/',views.dashboard_lifetime,name='dashboard_lifetime'),
    path('dashboard/this-year/',views.dashboard_this_year,name='dashboard_this_year'),
    path('dashboard/order-edit/',views.sale_edit,name='sale_edit'),
    path('dashboard/expense-edit/',views.expense_edit,name='expense_edit'),
    path('order/',views.sale_adder,name='sale_adder'),
    path('expense/',views.expense_adder,name='expense_adder'),
    path('profile/',views.profile,name='profile'),
    path('api/add-category/',views.api_add_category,name='api_add_category'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = views.page_not_found
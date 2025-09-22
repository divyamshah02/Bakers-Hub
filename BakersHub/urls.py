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
from django.urls import path,include
from BakersHub import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404
from django.views.generic import RedirectView

# from django.contrib.sitemaps.views import sitemap
# from BakersHub.sitemap import AllUrlsSitemap

# sitemaps = {
#     'all_urls':AllUrlsSitemap,
# }


urlpatterns = [
    # path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    
    # path('<path>/',views.maintenance,name='maintenance'),
    # --- Admin --- #
    path('admin/', admin.site.urls),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),
    path('report/',views.report,name='report'),
    path('freemium/',views.freemium,name='freemium'),
    
    # --- Website Pages --- #
    path('',views.home,name='home'),
    # path('blogs',views.blogs,name='blogs'),
    # path('about_us/',views.about_us,name='about_us'),
    # path('premium/',views.premium,name='premium'),
    path('privacy-policy/',views.privacy_policy,name='privacy_policy'),
    path('terms&conditions/',views.terms_conds,name='terms_conds'),
    
    # --------- App --------- #
    # --- Account --- #
    path('register/',views.register,name='register'),
    path('sign_in/',views.sign_in,name='sign_in'),
    path('forget_password/',views.forget_pass,name='forget_pass'),
    path('logout/', views.log_out, name='logout'),
    
    # --- Payment --- #
    # path('plans/',views.plans,name='plans'),
    # path('paymentsuccess/<int:no_days>',views.paymentsuccess,name='paymentsuccess'),
    
    # --- App Redirection --- #
    path('app/',views.app,name='app'),
    
    # --- Dashboard --- #
    path('dashboard/',views.dashboard,name='dashboard'),
    path('dashboard/last-month/',views.dashboard_last_month,name='dashboard_last_month'),
    path('dashboard/lifetime/',views.dashboard_lifetime,name='dashboard_lifetime'),
    path('dashboard/this-year/',views.dashboard_this_year,name='dashboard_this_year'),
    
    # --- Order Manager --- #
    path('order/',views.sale_adder,name='sale_adder'),
    path('order-edit/',views.sale_edit,name='sale_edit'),
    
    # --- Expense Manager --- #
    path('expense/',views.expense_adder,name='expense_adder'),
    path('expense-edit/',views.expense_edit,name='expense_edit'),
    
    # --- Charts --- #
    path('charts/',views.charts,name='charts'),
    
    # --- Shopping List --- #
    path('shopping_list/',views.shopping_list,name='shopping_list'),  
    
    # --- Task List --- #
    path('task_list/',views.task_list,name='task_list'),
    path('complete_task/<int:id>',views.complete_task,name='complete_task'),
    
    # --- Price Calculator --- #
    path('price_calculator/',views.price_calculator,name='price_calculator'),
    path('add_item/product/',views.add_item,name='add_item'),
    
    # --- Actions --- #  
    path('help/',views.help,name='help'),
    path('report_gen/',views.api_report_gen,name='api_report_gen'),
    path('profile/',views.profile,name='profile'),
    path('settings/',views.settings,name='settings'),
    path('delete_acc/',views.delete_acc,name='delete_acc'),
    
    # ------ API ------ #
    path('api/add-category/',views.api_add_category,name='api_add_category'),
    path('api/add-item/',views.api_add_item,name='api_add_item'),
    path('api/save-item/',views.api_save_item,name='api_save_item'),
    path('get_user_data/',views.get_all_users,name='api_get_user'),
    path('mic_clicked/',views.api_mic_click,name='mic_clicked'),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = views.page_not_found
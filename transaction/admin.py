from django.contrib import admin
from transaction.models import sales,expense
# Register your models here.

class AdminSales(admin.ModelAdmin):
    list_display = ('user_id','customer_name','order_name','quantity','qty_weigth','price','category','date_of_delivery','time_of_delivery','extra_note','order_date')

class AdminExpense(admin.ModelAdmin):
    list_display = ('user_id','expense_name','expense_amount','expense_quantity','qty_unit','extra_note','expense_date')

admin.site.register(sales,AdminSales)
admin.site.register(expense,AdminExpense)
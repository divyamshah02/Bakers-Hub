from django.contrib import admin
from user_0.models import UserProfile,Category,Expense,Sale,Ticket

# Register your models here.
class AdminUserProfile(admin.ModelAdmin):
    list_display = ('email','premium','user_id','pfp','otp','first_name','last_name')
    
admin.site.register(UserProfile,AdminUserProfile)

class AdminCategory(admin.ModelAdmin):
    list_display = ('user_id','category')
    
admin.site.register(Category,AdminCategory)

class AdminSales(admin.ModelAdmin):
    list_display = ('user_id','customer_name','order_name','quantity','qty_weigth','price','category','date_of_delivery','time_of_delivery','extra_note','order_date')

admin.site.register(Sale,AdminSales)

class AdminExpense(admin.ModelAdmin):
    list_display = ('user_id','expense_name','expense_amount','expense_quantity','qty_unit','extra_note','expense_date')

admin.site.register(Expense,AdminExpense)

class AdminTicket(admin.ModelAdmin):
    list_display = ('ticket_number','user_id','solved')
admin.site.register(Ticket,AdminTicket)
from django.contrib import admin
from user_0.models import UserProfile,Category,Expense,Sale,Ticket,ShoppingList,ItemShopping,TaskList,Product,ItemPrice

# Register your models here.
class AdminUserProfile(admin.ModelAdmin):
    list_display = ('email','user_id','pfp','premium','first_name','last_name')
admin.site.register(UserProfile,AdminUserProfile)

class AdminCategory(admin.ModelAdmin):
    list_display = ('user_id','category')
admin.site.register(Category,AdminCategory)

class AdminSales(admin.ModelAdmin):
    list_display = ('user_id','customer_name','order_name','quantity','qty_weigth','price','category','date_of_delivery','time_of_delivery','extra_note','order_date')
admin.site.register(Sale,AdminSales)

class AdminExpense(admin.ModelAdmin):
    list_display = ('user_id','expense_name','expense_amount','bill','expense_date')
admin.site.register(Expense,AdminExpense)

class AdminTicket(admin.ModelAdmin):
    list_display = ('ticket_number','user_id','solved')   
admin.site.register(Ticket,AdminTicket)

class AdminShoppingList(admin.ModelAdmin):
    list_display=('id','title','user_id')
admin.site.register(ShoppingList,AdminShoppingList)

class AdminItemShopping(admin.ModelAdmin):
    list_display = ('shopping_id','item','bought','added')
admin.site.register(ItemShopping,AdminItemShopping)

class AdminTaskList(admin.ModelAdmin):
    list_display = ('user_id','task','created','completed')
admin.site.register(TaskList,AdminTaskList)

class AdminProduct(admin.ModelAdmin):
    list_display = ('user_id','created','name')
admin.site.register(Product,AdminProduct)

class AdminItemPrice(admin.ModelAdmin):
    list_display = ('product_id','item','price','qty','qty_unit')
admin.site.register(ItemPrice,AdminItemPrice)
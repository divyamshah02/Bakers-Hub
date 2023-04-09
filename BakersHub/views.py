# SUPER-USER (divyamshah - navkar108)

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from user_0.models import UserProfile,Category,Expense,Sales
import random,datetime,yagmail,os

def home(request):    
    error = 0
    if request.method=="POST":        
            name = request.POST.get('name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            user_info = User.objects.filter(email=email)
            if len(user_info) == 0:
                new_id = True
                while new_id:
                    uid = random.randint(1111111111,9999999999)
                    if len(User.objects.filter(username = uid)) == 0:
                        new_id = False
                user = User.objects.create_user(username=uid,email=email,password=password)
                user.first_name = name
                user.save()
                user = authenticate(request, username=uid, password=password)
                login(request,user)
                request.session.set_expiry(30 * 24 * 60 * 60)                                             
                user_profile = UserProfile(user_id=user,email=email,first_name=name)
                user_profile.save()
                
                return redirect('dashboard')                
            else:
                error = 1
        
    
    data = {
        'error':error,
    }    
    return render(request, "index.html",data)

def page_not_found(request,exception):
    return render(request,'404.html',status=404)

def maintenance(request,path):    
    return render(request,'maintenance.html')

def premium(request):
    if request.method == "POST":
        print(request.POST.get('premium-email'))
        
    return render(request,'premium.html')

def register(request):
    error = 0
    if request.method=="POST":        
            name = request.POST.get('name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            user_info = User.objects.filter(email=email)
            if len(user_info) == 0:
                new_id = True
                while new_id:
                    uid = random.randint(1111111111,9999999999)
                    if len(User.objects.filter(username = uid)) == 0:
                        new_id = False
                user = User.objects.create_user(username=uid,email=email,password=password)
                user.first_name = name
                user.save()
                user = authenticate(request, username=uid, password=password)
                login(request,user)
                request.session.set_expiry(30 * 24 * 60 * 60)                                                 
                user_profile = UserProfile(user_id=user,email=email,first_name=name)
                user_profile.save()
                
                return redirect('dashboard')                
            else:
                error = 1
        
    
    data = {
        'error':error,
    }    
    return render(request, "register.html",data)

def sign_in(request):    
    error = 0
    email = None
    try :
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')      
            user_info = User.objects.filter(email=email)
            if len(user_info) > 0:
                username = user_info[0]   
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)                     
                    request.session.set_expiry(30 * 24 * 60 * 60)                                 
                    return redirect('dashboard')
                else:            
                    error = 2 #Wrong password                
            else:
                error = 1 #Not Register
    except:
        error = 3 #Fatal error
    data = {
        'error':error,
        'email':email,
    }
    return render(request,"app_sign_in.html",data)

def forget_pass(request):
    try:
        error = 0
        otp_sent = 0
        success = 0
        trial_round = 0              
        email = ''
        FROM_EMAIL = "divyamshah2020@gmail.com"
        PASSWORD = os.environ.get('password')
        print(os.environ.get('password'))
        if request.method == 'POST':
            if request.POST.get('email'):
                email = request.POST.get('email')
                user_exist = User.objects.filter(email=email)
                if len(user_exist) > 0:
                    try:
                        yag = yagmail.SMTP(FROM_EMAIL,PASSWORD)
                        otp = random.randint(111111,999999)
                        yag.send(to=email,subject="OTP - Verification",
                                    contents=[f"<h3><u>{otp}</u> is your otp to change password.</h3>"])
                        user_id = user_exist[0].username
                        UserProfile.objects.filter(user_id = user_id).update(otp = otp)                   
                        error = 0
                        otp_sent = 1     
                        trial_round = 1               
                    except:
                        error = 1 #Email was not sent
                else:
                    error = 2 #User does not exist                    
                            
            elif request.POST.get('otp'):
                user_otp = request.POST.get('otp')
                trial_round = request.POST.get('trial_round')                   
                email = request.POST.get('email_otp')
                user_id = User.objects.filter(email=email)[0].username
                real_otp = UserProfile.objects.filter(user_id=user_id)[0].otp
                if real_otp == user_otp:                
                    otp_sent = 2 #Correct OTP
                    success = 1
                else:
                    if trial_round == '1':
                        error = 3
                        otp_sent = 1 #Not Correct OTP                
                        trial_round = 2
                    else:
                        error = 4 #Wrong OTP     
                    
            elif request.POST.get('new_password'):   
                new_password = request.POST.get('new_password')   
                email = request.POST.get('email_password')
                user = User.objects.get(email = email)
                user.set_password(new_password)   
                UserProfile.objects.filter(user_id = user).update(otp = 0) 
                user.save()
                success = 2
    except:
        error = 1
        otp_sent = 0
        success = 0
        trial_round = 0              
        email = ''                  
                
    data = {
        'error':error,
        'otp_sent':otp_sent,
        'success':success,
        'trial_round':trial_round,
        'email':email,
    }        
    return render(request,'forget_pass.html',data) 

def log_out(request):
    logout(request)
    return redirect('sign_in')

@login_required(login_url=reverse_lazy('sign_in'))
def dashboard(request):    
    try:                
        if request.session.get_expiry_age() <= 0:
            request.session.set_expiry(30 * 24 * 60 * 60)
        user = request.user      
        if request.method == 'POST':
            if request.POST.get('sale_edit'):
                request.session['sale_id'] = request.POST.get('sale_edit')
                return redirect('sale_edit')
            elif request.POST.get('sale_delete'):
                Sales.objects.filter(id=request.POST.get('sale_delete')).delete()
            elif request.POST.get('exp_edit'):
                request.session['expense_id'] = request.POST.get('exp_edit')
                return redirect('expense_edit')
            elif request.POST.get('exp_delete'):
                Expense.objects.filter(id=request.POST.get('exp_delete')).delete()        
        current_date = datetime.date.today()
        month_num = current_date.strftime("%m")
        month = current_date.strftime("%B")
        year = current_date.strftime("%Y")
            
        # --- Sale Data --- #
        user_sale_data = Sales.objects.filter(user_id = user)
        user_sale_info = []
        user_sale_total_amt = 0
        for user_sales in user_sale_data:
            sale_date = user_sales.order_date.split('-')
            if sale_date[1] == month_num:
                temp_sale_data = {
                    'customer':str(user_sales.customer_name).title(),
                    'item':f"{(user_sales.order_name).title()} ({user_sales.quantity} {user_sales.qty_weigth})",
                    'date':user_sales.order_date,
                    'date_of_delivery':user_sales.date_of_delivery,
                    'price':user_sales.price,
                    'notes':user_sales.extra_note,
                    'id':user_sales.id,
                }
                user_sale_total_amt += int(user_sales.price)
                user_sale_info.append(temp_sale_data)
        
        # --- Expense Data --- #            
        user_expense_data = Expense.objects.filter(user_id = user)
        user_expense_info = []
        user_expense_total_amt = 0
        for user_expense in user_expense_data:
            expense_date = user_expense.expense_date.split('-')
            if expense_date[1] == month_num:
                temp_expense_data = {
                    'item':str(user_expense.expense_name).title(),
                    'qty':f"{user_expense.expense_quantity} {user_expense.qty_unit}",
                    'date':user_expense.expense_date,
                    'price':user_expense.expense_amount,
                    'id':user_expense.id,
                    'notes':user_expense.extra_note,
                }
                user_expense_total_amt += int(user_expense.expense_amount)
                user_expense_info.append(temp_expense_data)
            
        # --- Constants --- #
        profit = user_sale_total_amt - user_expense_total_amt
        formatted_profit = "{:,.0f}".format(profit)
        
        formatted_user_expense_total_amt = "{:,.0f}".format(user_expense_total_amt)
        formatted_user_sale_total_amt = "{:,.0f}".format(user_sale_total_amt)
        
        # --- Ratio --- #
        if profit > 0:
            profit_perct = int((profit*100) / user_sale_total_amt) 
            loss_perct = None
        elif profit < 0:  
            if user_sale_total_amt == 0:
                profit_perct = 0
                loss_perct = 100                
            else: 
                profit_perct = int((profit*100) / user_sale_total_amt) 
                loss_perct = profit_perct * -1
        else:
            profit_perct = 0
            loss_perct = 0    
            
        if UserProfile.objects.filter(user_id=user)[0].pfp == "":
            profile_pfp = 0 
        else:    
            profile_pfp = UserProfile.objects.filter(user_id=user)[0].pfp.url       
        
        if len(user_expense_info) == 0:
            no_exp = 1
        else:
            no_exp = 0
        if len(user_sale_info) == 0:
            no_sale = 1
        else:
            no_sale = 0
        data = {
            'tab':1,
            'user':user,
            'expense_info':user_expense_info,
            'no_exp':no_exp,
            'sale_info':user_sale_info,
            'no_sale':no_sale,
            'profit':formatted_profit,
            'profit_perct':profit_perct,
            'loss_perct':loss_perct,
            'sales':formatted_user_sale_total_amt,
            'payments':formatted_user_expense_total_amt,
            'orders':len(user_sale_info),
            'month':month,
            'year':year,
            'p_letter':str(user.first_name)[0].lower(),
            'profile_pfp':profile_pfp,
        }        
        return render(request,"dashboard.html",data)        
    except:
        return redirect('sign_in')

@login_required(login_url=reverse_lazy('sign_in'))
def dashboard_last_month(request):
    try:
        if request.user.is_authenticated:
            if request.session.get_expiry_age() <= 0:
                request.session.set_expiry(30 * 24 * 60 * 60)
            user = request.user    
            if request.method == 'POST':
                if request.POST.get('sale_edit'):
                    request.session['sale_id'] = request.POST.get('sale_edit')
                    return redirect('sale_edit')
                elif request.POST.get('sale_delete'):
                    Sales.objects.filter(id=request.POST.get('sale_delete')).delete()
                elif request.POST.get('exp_edit'):
                    request.session['expense_id'] = request.POST.get('exp_edit')
                    return redirect('expense_edit')
                elif request.POST.get('exp_delete'):
                    Expense.objects.filter(id=request.POST.get('exp_delete')).delete()
                
            current_date = datetime.date.today()
            month = int(current_date.strftime("%m"))
            year = int(current_date.strftime("%Y"))
            if month == 1:
                month = 13
                year = year-1   
            last_month = datetime.date(year= year, month=month-1, day=1)
            month = last_month.strftime("%B")
            month_num = last_month.strftime("%m")
            year = last_month.strftime("%Y")
            
            # --- Sale Data --- #
            user_sale_data = Sales.objects.filter(user_id = user)
            user_sale_info = []
            user_sale_total_amt = 0
            for user_sales in user_sale_data:
                sale_date = user_sales.order_date.split('-')
                if sale_date[1] == month_num:
                    temp_sale_data = {
                        'customer':str(user_sales.customer_name).title(),
                        'item':f"{(user_sales.order_name).title()} ({user_sales.quantity} {user_sales.qty_weigth})",
                        'date':user_sales.order_date,
                        'notes':user_sales.extra_note,                        
                        'price':user_sales.price,
                        'id':user_sales.id,                
                    }
                    user_sale_total_amt += int(user_sales.price)
                    user_sale_info.append(temp_sale_data)
            
            # --- Expense Data --- #            
            user_expense_data = Expense.objects.filter(user_id = user)
            user_expense_info = []
            user_expense_total_amt = 0
            for user_expense in user_expense_data:
                expense_date = user_expense.expense_date.split('-')
                if expense_date[1] == month_num:
                    temp_expense_data = {
                        'item':str(user_expense.expense_name).title(),
                        'qty':f"{user_expense.expense_quantity} {user_expense.qty_unit}",
                        'date':user_expense.expense_date,
                        'price':user_expense.expense_amount,
                        'id':user_expense.id,              
                        'notes':user_expense.extra_note,
  
                    }
                    user_expense_total_amt += int(user_expense.expense_amount)
                    user_expense_info.append(temp_expense_data)
                
            # --- Constants --- #
            profit = user_sale_total_amt - user_expense_total_amt
            formatted_profit = "{:,.0f}".format(profit)
            

            formatted_user_expense_total_amt = "{:,.0f}".format(user_expense_total_amt)
            formatted_user_sale_total_amt = "{:,.0f}".format(user_sale_total_amt)
            
            # --- Ratio --- #
            if profit > 0:
                profit_perct = int((profit*100) / user_sale_total_amt) 
                loss_perct = None
                
            elif profit < 0:   
                if user_sale_total_amt == 0:
                    profit_perct = 0
                    loss_perct = 100                            
                else:
                    profit_perct = int((profit*100) / user_sale_total_amt) 
                    loss_perct = profit_perct * -1
            else:
                profit_perct = 0
                loss_perct = 0     
                
            if UserProfile.objects.filter(user_id=user)[0].pfp == "":
                profile_pfp = 0 
            else:    
                profile_pfp = UserProfile.objects.filter(user_id=user)[0].pfp.url    
            
            data = {
                'tab':1,
                'user':user,
                'expense_info':user_expense_info,
                'sale_info':user_sale_info,
                'profit':formatted_profit,
                'profit_perct':profit_perct,
                'loss_perct':loss_perct,
                'sales':formatted_user_sale_total_amt,
                'payments':formatted_user_expense_total_amt,
                'orders':len(user_sale_info),
                'month':month,
                'year':year,
                'p_letter':str(user.first_name)[0].lower(), 
                'profile_pfp':profile_pfp,                  
            }
            return render(request,"dashboard.html",data)
        
    except:
        return redirect('dashboard')

@login_required(login_url=reverse_lazy('sign_in'))
def dashboard_this_year(request):
    try:
        if request.user.is_authenticated:
            if request.session.get_expiry_age() <= 0:
                request.session.set_expiry(30 * 24 * 60 * 60)
        user = request.user
        if request.method == 'POST':
            if request.POST.get('sale_edit'):
                request.session['sale_id'] = request.POST.get('sale_edit')
                return redirect('sale_edit')
            elif request.POST.get('sale_delete'):
                Sales.objects.filter(id=request.POST.get('sale_delete')).delete()
            elif request.POST.get('exp_edit'):
                request.session['expense_id'] = request.POST.get('exp_edit')
                return redirect('expense_edit')
            elif request.POST.get('exp_delete'):
                Expense.objects.filter(id=request.POST.get('exp_delete')).delete()
            
        current_date = datetime.date.today()
        year = current_date.strftime("%Y")
        
        
        # --- Sale Data --- #
        user_sale_data = Sales.objects.filter(user_id = user)
        user_sale_info = []
        user_sale_total_amt = 0
        for user_sales in user_sale_data:
            sale_date = user_sales.order_date.split('-')
            if sale_date[0] == year:
                temp_sale_data = {
                    'customer':str(user_sales.customer_name).title(),
                    'item':f"{(user_sales.order_name).title()} ({user_sales.quantity} {user_sales.qty_weigth})",
                    'date':user_sales.order_date,
                    'notes':user_sales.extra_note,
                    'price':user_sales.price,
                    'id':user_sales.id,                
                }
                user_sale_total_amt += int(user_sales.price)
                user_sale_info.append(temp_sale_data)
        
        # --- Expense Data --- #            
        user_expense_data = Expense.objects.filter(user_id = user)
        user_expense_info = []
        user_expense_total_amt = 0
        for user_expense in user_expense_data:
            expense_date = user_expense.expense_date.split('-')
            if expense_date[0] == year:
                temp_expense_data = {
                    'item':str(user_expense.expense_name).title(),
                    'qty':f"{user_expense.expense_quantity} {user_expense.qty_unit}",
                    'date':user_expense.expense_date,
                    'price':user_expense.expense_amount,
                    'id':user_expense.id,          
                    'notes':user_expense.extra_note,      
                }
                user_expense_total_amt += int(user_expense.expense_amount)
                user_expense_info.append(temp_expense_data)
            
        # --- Constants --- #
        profit = user_sale_total_amt - user_expense_total_amt
        formatted_profit = "{:,.0f}".format(profit)
        

        formatted_user_expense_total_amt = "{:,.0f}".format(user_expense_total_amt)
        formatted_user_sale_total_amt = "{:,.0f}".format(user_sale_total_amt)
        
        # --- Ratio --- #
        if profit > 0:
            profit_perct = int((profit*100) / user_sale_total_amt) 
            loss_perct = None
            
        elif profit < 0:   
            if user_sale_total_amt == 0:
                profit_perct = 0
                loss_perct = 100                            
            else:
                profit_perct = int((profit*100) / user_sale_total_amt) 
                loss_perct = profit_perct * -1
        else:
            profit_perct = 0
            loss_perct = 0    
            
        if UserProfile.objects.filter(user_id=user)[0].pfp == "":
            profile_pfp = 0 
        else:    
            profile_pfp = UserProfile.objects.filter(user_id=user)[0].pfp.url     
        
        data = {
            'tab':1,
            'user':user,
            'expense_info':user_expense_info,
            'sale_info':user_sale_info,
            'profit':formatted_profit,
            'profit_perct':profit_perct,
            'loss_perct':loss_perct,
            'sales':formatted_user_sale_total_amt,
            'payments':formatted_user_expense_total_amt,
            'orders':len(user_sale_info),
            'month':year,
            'year':'Data',
            'p_letter':str(user.first_name)[0].lower(),        
            'profile_pfp':profile_pfp,       
        }
        return render(request,"dashboard.html",data)
    except:
        return redirect('dashboard')

@login_required(login_url=reverse_lazy('sign_in'))
def dashboard_lifetime(request):
    try:
        if request.user.is_authenticated:
            if request.session.get_expiry_age() <= 0:
                request.session.set_expiry(30 * 24 * 60 * 60)
        user = request.user
        if request.method == 'POST':
            if request.POST.get('sale_edit'):
                request.session['sale_id'] = request.POST.get('sale_edit')
                return redirect('sale_edit')
            elif request.POST.get('sale_delete'):
                Sales.objects.filter(id=request.POST.get('sale_delete')).delete()
            elif request.POST.get('exp_edit'):
                request.session['expense_id'] = request.POST.get('exp_edit')
                return redirect('expense_edit')
            elif request.POST.get('exp_delete'):
                Expense.objects.filter(id=request.POST.get('exp_delete')).delete()
        
        # --- Sale Data --- #
        user_sale_data = Sales.objects.filter(user_id = user)
        user_sale_info = []
        user_sale_total_amt = 0
        for user_sales in user_sale_data:
            temp_sale_data = {
                    'customer':str(user_sales.customer_name).title(),
                    'item':f"{(user_sales.order_name).title()} ({user_sales.quantity} {user_sales.qty_weigth})",
                    'date':user_sales.order_date,
                    'notes':user_sales.extra_note,
                    'price':user_sales.price,
                    'id':user_sales.id,                
                }
            user_sale_total_amt += int(user_sales.price)
            user_sale_info.append(temp_sale_data)
        
        # --- Expense Data --- #            
        user_expense_data = Expense.objects.filter(user_id = user)
        user_expense_info = []
        user_expense_total_amt = 0
        for user_expense in user_expense_data:
            expense_date = user_expense.expense_date.split('-')
            temp_expense_data = {
                    'item':str(user_expense.expense_name).title(),
                    'qty':f"{user_expense.expense_quantity} {user_expense.qty_unit}",
                    'date':user_expense.expense_date,
                    'price':user_expense.expense_amount,
                    'id':user_expense.id,    
                    'notes':user_expense.extra_note,            
                }
            user_expense_total_amt += int(user_expense.expense_amount)
            user_expense_info.append(temp_expense_data)
            
        # --- Constants --- #
        profit = user_sale_total_amt - user_expense_total_amt
        formatted_profit = "{:,.0f}".format(profit)
        

        formatted_user_expense_total_amt = "{:,.0f}".format(user_expense_total_amt)
        formatted_user_sale_total_amt = "{:,.0f}".format(user_sale_total_amt)
        
        # --- Ratio --- #
        if profit > 0:
            profit_perct = int((profit*100) / user_sale_total_amt) 
            loss_perct = None
            
        elif profit < 0:   
            if user_sale_total_amt == 0:
                profit_perct = 0
                loss_perct = 100                            
            else:
                profit_perct = int((profit*100) / user_sale_total_amt) 
                loss_perct = profit_perct * -1
        else:
            profit_perct = 0
            loss_perct = 0  
        
        if UserProfile.objects.filter(user_id=user)[0].pfp == "":
            profile_pfp = 0 
        else:    
            profile_pfp = UserProfile.objects.filter(user_id=user)[0].pfp.url       
        
        data = {
            'tab':1,
            'user':user,
            'expense_info':user_expense_info,
            'sale_info':user_sale_info,
            'profit':formatted_profit,
            'profit_perct':profit_perct,
            'loss_perct':loss_perct,
            'sales':formatted_user_sale_total_amt,
            'payments':formatted_user_expense_total_amt,
            'orders':len(user_sale_info),
            'month':"Lifetime",
            'year':"Data",
            'p_letter':str(user.first_name)[0].lower(),  
            'profile_pfp':profile_pfp,       
        
        }
        return render(request,"dashboard.html",data)
    except:
        return redirect('dashboard')

@login_required(login_url=reverse_lazy('sign_in'))
def sale_edit(request):
    try:
        user = request.user
        sale_edit = None
        if request.method == "POST":
            try:            
                request.session['sale_id'] = request.POST.get('sale_id')           
                Sales.objects.filter(id = request.session.get('sale_id')).update(
                                    customer_name=request.POST.get('customer_name'),
                                    order_name=request.POST.get('order_name'),
                                    quantity=request.POST.get('quantity'),
                                    qty_weigth=request.POST.get('unit'),
                                    price=request.POST.get('price'),
                                    date_of_delivery=request.POST.get('date_of_delivery'),
                                    time_of_delivery=request.POST.get('time_of_delivery'),
                                    extra_note=request.POST.get('extra_note'),
                                    order_date=request.POST.get('order_date'),
                                    category=request.POST.get('category'),
                                    )
                sale_edit = {
                    'customer_name':request.POST.get('customer_name'),
                    'order_name':request.POST.get('order_name'),
                    'quantity':request.POST.get('quantity'),
                    'unit':request.POST.get('unit'),
                    'price':request.POST.get('price'),
                    'date_of_delivery':request.POST.get('date_of_delivery'),
                    'time_of_delivery':request.POST.get('time_of_delivery'),                
                }
            except:
                sale_edit = 1
        if(request.session.get('sale_id')) is None:
            return redirect('dashboard')
        
        else:
            sale_id = request.session.get('sale_id')
            sale_data = Sales.objects.filter(id = sale_id)[0]
            if UserProfile.objects.filter(user_id=user)[0].pfp == "":
                profile_pfp = 0 
            else:    
                profile_pfp = UserProfile.objects.filter(user_id=user)[0].pfp.url 
            category_data = Category.objects.filter(user_id = user)
            data = {
                'customer_name':sale_data.customer_name,
                'order_name':sale_data.order_name,
                'quantity':sale_data.quantity,
                'weight':sale_data.qty_weigth,
                'price':sale_data.price,
                'category':sale_data.category,
                'category_data':category_data,
                'category_len':len(category_data),
                'date_of_delivery':sale_data.date_of_delivery,
                'time_of_delivery':sale_data.time_of_delivery,
                'extra_notes':str(sale_data.extra_note).strip(),
                'order_date':sale_data.order_date,
                'sale':sale_edit,
                'id':sale_id,
                'p_letter':str(user.first_name)[0].lower(),
                'profile_pfp':profile_pfp,       

            }       
            request.session['sale_id'] = None
            return render(request,'sale_edit.html',data)  
    except:
        return redirect('dashboard')  

@login_required(login_url=reverse_lazy('sign_in'))
def sale_adder(request):
    try:
        sale_add = None
        user = request.user
        if request.method == "POST":         
            try:               
                add_sale = Sales(user_id = user,
                                    customer_name=request.POST.get('customer_name'),
                                    order_name=request.POST.get('order_name'),
                                    quantity=request.POST.get('quantity'),
                                    qty_weigth=request.POST.get('unit'),
                                    price=request.POST.get('price'),
                                    date_of_delivery=request.POST.get('date_of_delivery'),
                                    time_of_delivery=request.POST.get('time_of_delivery'),
                                    extra_note=request.POST.get('extra_note'),
                                    order_date=request.POST.get('order_date'),
                                    category=request.POST.get('category'),
                                    )
                add_sale.save()
                sale_add = {
                    'customer_name':request.POST.get('customer_name'),
                    'order_name':request.POST.get('order_name'),
                    'quantity':request.POST.get('quantity'),
                    'unit':request.POST.get('unit'),
                    'price':request.POST.get('price'),
                    'date_of_delivery':request.POST.get('date_of_delivery'),
                    'time_of_delivery':request.POST.get('time_of_delivery'),                
                }
            except:
                sale_add = 1
                
        if UserProfile.objects.filter(user_id=user)[0].pfp == "":
            profile_pfp = 0 
        else:    
            profile_pfp = UserProfile.objects.filter(user_id=user)[0].pfp.url 
            
        category_data = Category.objects.filter(user_id = user)
        data = {
            'tab':2,
            'sale':sale_add,
            'p_letter':str(user.first_name)[0].lower(),    
            'profile_pfp':profile_pfp,       
            'user':user,
            'category_data':category_data,
            'category_len':len(category_data),
                
        }
        return render(request,"sale_adder.html",data)
    except:
        return redirect('dashboard')
    
@login_required(login_url=reverse_lazy('sign_in'))
def expense_edit(request):
    try:
        user = request.user
        expense_edit = None
        if request.method == 'POST': 
            try:       
                request.session['expense_id'] = request.POST.get('exp_id')           
                Expense.objects.filter(id=request.session.get('expense_id')).update(
                                        expense_name = request.POST.get('expense_name'),
                                        expense_amount = request.POST.get('expense_amount'),
                                        expense_quantity =request.POST.get('expense_quantity'),
                                        qty_unit = request.POST.get('qty_unit'),
                                        extra_note = request.POST.get('extra_note'),
                                        expense_date = request.POST.get('expense_date'),
                                    )
                expense_edit = {
                    'name': request.POST.get('expense_name'),
                    'price':request.POST.get('expense_amount'),
                    'qty':request.POST.get('expense_quantity'),
                    'unit':request.POST.get('qty_unit'),
                    'date':request.POST.get('expense_date'),
                }
            except:
                expense_edit = 1
        if(request.session.get('expense_id')) is None:
            return redirect('dashboard')
        else:
            expense_id = request.session.get('expense_id')
            expense_data = Expense.objects.filter(id = expense_id)[0]
            if UserProfile.objects.filter(user_id=user)[0].pfp == "":
                profile_pfp = 0 
            else:    
                profile_pfp = UserProfile.objects.filter(user_id=user)[0].pfp.url 
            data = {
                'expense_name':expense_data.expense_name,
                'expense_amount':expense_data.expense_amount,
                'quantity':expense_data.expense_quantity,
                'weight':expense_data.qty_unit,                      
                'extra_notes':str(expense_data.extra_note).strip(),
                'expense_date':expense_data.expense_date,
                'expense':expense_edit,
                'id':expense_id,
                'p_letter':str(user.first_name)[0].lower(),
                'profile_pfp':profile_pfp,       

            }       
            request.session['expense_id'] = None
            return render(request,'expense_edit.html',data)   
    except:
        return redirect('dashboard')
    
@login_required(login_url=reverse_lazy('sign_in'))
def expense_adder(request):
    try:
        expense_add = None
        user = request.user
        if request.method == 'POST': 
            try:       
                add_expense = Expense(user_id = user,
                                        expense_name = request.POST.get('expense_name'),
                                        expense_amount = request.POST.get('expense_amount'),
                                        expense_quantity =request.POST.get('expense_quantity'),
                                        qty_unit = request.POST.get('qty_unit'),
                                        extra_note = request.POST.get('extra_note'),
                                        expense_date = request.POST.get('expense_date'),
                                    )
                add_expense.save()
                expense_add = {
                    'name': request.POST.get('expense_name'),
                    'price':request.POST.get('expense_amount'),
                    'qty':request.POST.get('expense_quantity'),
                    'unit':request.POST.get('qty_unit'),
                    'date':request.POST.get('expense_date'),
                }
            except:
                expense_add = 1
        if UserProfile.objects.filter(user_id=user)[0].pfp == "":
            profile_pfp = 0 
        else:    
            profile_pfp = UserProfile.objects.filter(user_id=user)[0].pfp.url
        data = {
            'tab':3,
            'expense':expense_add,
            'p_letter':str(user.first_name)[0].lower(),  
            'profile_pfp':profile_pfp,       
                
        }
        return render(request,"expense_adder.html",data)
    except:
        return redirect('dashboard')
    
@login_required(login_url=reverse_lazy('sign_in'))
def profile(request):
    try:
        user = request.user
        if request.method == 'POST':
            if request.POST.get('pfp_changed') == 'True':            
                user_profile_pfp=UserProfile.objects.get(user_id = user)
                user_profile_pfp.pfp = request.FILES.get('pfp')
                user_profile_pfp.save()
            request.user.first_name = request.POST.get('first_name')
            request.user.last_name = request.POST.get('last_name')
            user.save()
            
            user_profile = UserProfile.objects.get(user_id = user)
            user_profile.first_name = request.POST.get('first_name')
            user_profile.last_name = request.POST.get('last_name')
            
        if UserProfile.objects.filter(user_id=user)[0].pfp == "":
            profile_pfp = 0 
        else:    
            profile_pfp = UserProfile.objects.filter(user_id=user)[0].pfp.url
        data = {
            'first_name':request.user.first_name,
            'last_name':request.user.last_name,
            'email':request.user.email,
            'p_letter':str(user.first_name)[0].lower(), 
            'profile_pfp':profile_pfp,       
                
        }
        return render(request,'profile.html',data)
    except:
        return redirect('dashboard')

#API
def api_add_category(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        user_id = request.POST.get('user_id')
        category_add = Category(category=category,user_id=user_id)
        category_add.save()
        return JsonResponse({'success': True})

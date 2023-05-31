# SUPER-USER (divyam - navkar108)

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.db.models import Count
from user_0.models import UserProfile,Category,Expense,Sales
from django.core.files.uploadedfile import InMemoryUploadedFile
import random,datetime,yagmail,os
from PIL import Image
from io import BytesIO
from BakersHub.email_sent import SendMailOTP

def error_log(error,user,url):
    with open("error_log.txt",'a') as error_file:
        date_time = datetime.datetime.now()
        error_file.write(f'[{date_time}] -> [{user}/{user.first_name}] : [{url}] [{error}] - At Line {(error.__traceback__).tb_lineno}\n')
        # File name - tb_frame.f_code.co_filename

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

def about_us(request):
    return render(request,"about_us.html")

def page_not_found(request,exception):
    return render(request,'404.html',status=404)
   
def maintenance(request,path):    
    return render(request,'maintenance.html')

def premium(request):
    if request.method == "POST":
        print(request.POST.get('premium-email'))
        
    return render(request,'premium.html')

def register(request):
    error = 0 #No Error
    if request.method=="POST":   
            # Storing details in variables     
            name = request.POST.get('name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            join_date = (datetime.date.today()).strftime("%d/%m/%Y")
            user_free_end_date = datetime.date.today()+datetime.timedelta(days=14)
            free_end_date = user_free_end_date.strftime("%d/%m/%y")
            user_info = User.objects.filter(email=email) #Collecting Information
            if len(user_info) == 0:
                # User is not registered
                new_id = True
                # This loop is for generating unique User Id 
                while new_id:
                # It checks user id is already used if yes than generates new id
                    uid = random.randint(1111111111,9999999999)
                    if len(User.objects.filter(username = uid)) == 0:
                        new_id = False
                # Creating new user
                user = User.objects.create_user(username=uid,email=email,password=password)
                user.first_name = name # Saving name
                user.save()
                # Logging user
                user = authenticate(request, username=uid, password=password)
                login(request,user)
                request.session.set_expiry(30 * 24 * 60 * 60) # Storing user data in session (remembering the user)
                # Saving the user data in database (own - BH)                                               
                user_profile = UserProfile(user_id=user,email=email,first_name=name,join_date=join_date,free_end_date=free_end_date)
                user_profile.save()
                
                return redirect('dashboard')                
            else:
                # User is already registered
                error = 1
        
    data = {
        'error':error,
    }    
    return render(request, "register.html",data)

def sign_in(request):    
    error = 0 # No error
    email = None # For validation in html
    try :
        if request.method == 'POST':
            # Storing data in variables
            email = request.POST.get('email')
            password = request.POST.get('password')      
            user_info = User.objects.filter(email=email) # Checking user in database
            if len(user_info) > 0:
                # User data is available
                username = user_info[0] # It is an object that stores user id
                user = authenticate(request, username=username, password=password) # Authenticating user
                if user is not None:
                    # User is authenticated
                    login(request, user)                     
                    request.session.set_expiry(30 * 24 * 60 * 60) # Storing user data in session (remembering the user)                               
                    return redirect('dashboard')
                else:            
                    error = 2 # Wrong password                
            else:
                error = 1 # Not Register
    except:
        error = 3 # Fatal error
    data = {
        'error':error,
        'email':email,
    }
    return render(request,"app_sign_in.html",data)

def forget_pass(request):
    try:
        # Temp values for validation in html
        error = 0
        otp_sent = 0
        success = 0
        trial_round = 0              
        email = ''
        mail_sender = SendMailOTP()
        if request.method == 'POST':
            # First page view - (here user will enter their email id)
            if request.POST.get('email'):
                email = request.POST.get('email')
                user_exist = User.objects.filter(email=email) # Checking if user's email is registered
                if len(user_exist) > 0:
                    # user has an account (egistered)
                    otp = random.randint(111111,999999) # Generating OTP of 6 digits
                    sent_mail = mail_sender.send(email=email,otp=otp)
                    
                    if sent_mail:
                            user_id = user_exist[0].username
                            UserProfile.objects.filter(user_id = user_id).update(otp = otp)                   
                            error = 0 # No error
                            otp_sent = 1 # otp is sent to email & saved in database
                            trial_round = 1 # Users gets 2 trial and here it is first
                    else:
                        error = 1 # Email was not sent
                else:
                    error = 2 # User does not exist                    
            # Second page view - (here user will enter otp sent to their email)                
            elif request.POST.get('otp'):
                user_otp = request.POST.get('otp') # User entered otp
                trial_round = request.POST.get('trial_round') # user gets 2 trails for otp it is sent from input tag in html             
                email = request.POST.get('email_otp')
                user_id = User.objects.filter(email=email)[0].username # storing user id
                real_otp = UserProfile.objects.filter(user_id=user_id)[0].otp # Getting real otp from database
                # Checking if otp entered is correct
                if real_otp == user_otp:                
                    otp_sent = 2 # Correct OTP
                    success = 1 # Success 1 means user can change password 
                else:
                    if trial_round == '1':
                        # If it is first trial round 
                        error = 3 # Wrong otp but try one more time
                        otp_sent = 1 # Enter otp again              
                        trial_round = 2 # 2nd trial round is last round
                    else:
                        error = 4 # Wrong OTP but no more chance to re enter   
            # Third page view - (here user will enter new password)                                    
            elif request.POST.get('new_password'):   
                # Storing usee new password
                new_password = request.POST.get('new_password')   
                email = request.POST.get('email_password')
                user = User.objects.get(email = email) # Getting user object
                user.set_password(new_password) # Setting new password
                UserProfile.objects.filter(user_id = user).update(otp = 0) # Changing the otp field in database
                user.save()
                success = 2 # Password has been changed
    
    except:
        error = 1 # Fatal Error
        otp_sent = 0 # For validation
        success = 0 # No success
        trial_round = 0 # For validation     
        email = '' # Null email
                
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

def app(request):
    try:
        user=request.user
        user_view = UserProfile.objects.filter(user_id=user)[0].first_view
        if user_view == '1':
            return redirect('dashboard')
        if user_view == '2':
            return redirect('sale_adder')
        if user_view == '3':
            return redirect('expense_adder')
    except:
        return redirect('sign_in')

def check_pre_expr(user):
    user_profile = UserProfile.objects.get(user_id=user)
    today = datetime.date.today()
    end_date = user_profile.premium_end_date
    if end_date != '0':
        end_date = str(user_profile.premium_end_date).split('/')
        end_date = datetime.date(day=int(end_date[0]),month=int(end_date[1]),year=int(end_date[2]))
        if today > end_date:
            return False
        else:
            days_remaining = end_date - today            
            return int(days_remaining.days)
    
@login_required(login_url=reverse_lazy('sign_in'))
def plans(request):
    user=request.user
    user_profile = UserProfile.objects.filter(user_id=user)[0]
    
    is_premium = user_profile.premium
    if is_premium == False:
        user_free_date_lst = str(user_profile.free_end_date).split('/')
        user_free_end_date = datetime.date(day=int(user_free_date_lst[0]),month=int(user_free_date_lst[1]),year=int(str("20")+str(user_free_date_lst[2])))
        today = datetime.date.today()
        if today <= user_free_end_date:
            remaining_days = (user_free_end_date - today).days
        else:        
            remaining_days = None   
        premium_ended = None
    else:
        premium_is = check_pre_expr(user)
        if premium_is == False:
            premium_ended = True
        else:
            if premium_is <=5:
                premium_ended = premium_is
            else:
                premium_ended = False
        
        remaining_days = None
    
    profile_pfp = user_profile.pfp
    if profile_pfp == "":
        profile_pfp = 0 
    else:    
        profile_pfp = profile_pfp.url 

    today = datetime.date.today()
    day_30 = (today + datetime.timedelta(days=30)).strftime("%d %B, %Y")
    day_90 = (today + datetime.timedelta(days=90)).strftime("%d %B, %Y")
    day_180 = (today + datetime.timedelta(days=180)).strftime("%d %B, %Y")
        
    data={
        'p_letter':str(user.first_name)[0].lower(), 
        'profile_pfp':profile_pfp,  
        'is_premium':is_premium,  
        'remaining_days':remaining_days,
        'theme':user_profile.theme_selection,
        'premium_ended':premium_ended,
        'day_30':day_30,
        'day_90':day_90,
        'day_180':day_180,
    }
    return render(request,'plans.html',data)

@login_required(login_url=reverse_lazy('sign_in'))
def paymentsuccess(request,no_days):
    user = request.user
    user_profile = UserProfile.objects.get(user_id=user)
    today = datetime.date.today()
    end_date = today + datetime.timedelta(days=no_days)
    today=today.strftime("%d/%m/%Y")
    end_date=end_date.strftime("%d/%m/%Y")
    user_profile.premium_start_date = today
    user_profile.premium_end_date = end_date
    user_profile.premium_month_plan = no_days
    user_profile.premium = True
    user_profile.payment_id = request.GET.get('payment_id')
    user_profile.save()
    return redirect('dashboard')

@login_required(login_url=reverse_lazy('sign_in'))
def dashboard(request):    
    try:                                
        # Remembering the user in session
        if request.session.get_expiry_age() <= 0:
            # If the session will expire
            request.session.set_expiry(30 * 24 * 60 * 60)
        user = request.user # Storing user
        user_profile = UserProfile.objects.filter(user_id=user)[0]        
        is_premium = user_profile.premium
        if is_premium == False:
            user_free_date_lst = str(user_profile.free_end_date).split('/')
            user_free_end_date = datetime.date(day=int(user_free_date_lst[0]),month=int(user_free_date_lst[1]),year=int(str("20")+str(user_free_date_lst[2])))
            today = datetime.date.today()
            if today <= user_free_end_date:
                remaining_days = (user_free_end_date - today).days
            else:
                return redirect('plans')
            premium_ended = None
        else:
            premium_is = check_pre_expr(user)
            if premium_is == False:
                premium_ended = True
                return redirect('plans')
            else:
                if premium_is <=5:
                    premium_ended = premium_is
                else:
                    premium_ended = False
            
            remaining_days = None
        if request.method == 'POST':
            if request.POST.get('sale_edit'):
                # Getting id of sale for editing
                request.session['sale_id'] = request.POST.get('sale_edit') # Storing sale data in session
                return redirect('sale_edit')
            
            elif request.POST.get('sale_delete'):
                # Getting id of sale for deleting                
                Sales.objects.filter(id=request.POST.get('sale_delete')).delete() # Deleting sale data
                
            elif request.POST.get('exp_edit'):
                # Getting id of exp for editing
                request.session['expense_id'] = request.POST.get('exp_edit') # Storing exp data in session
                return redirect('expense_edit')
            
            elif request.POST.get('exp_delete'):
                # Getting id of exp for deleting
                Expense.objects.filter(id=request.POST.get('exp_delete')).delete() # Deleting exp data
                       
        current_date = datetime.date.today() # Getting current data
        month_num = current_date.strftime("%m") # Storing month num
        month = current_date.strftime("%B") # Storing month
        year = current_date.strftime("%Y") # Storing year
            
        # --- Getting Sale Data --- #
        user_sale_data = Sales.objects.filter(user_id = user) # All sale information from database of user
        # Initializing Variables
        user_sale_info = []
        user_sale_total_amt = 0        
        for user_sales in user_sale_data:
            sale_date = user_sales.order_date.split('-') # Getting month num from Sale date
            if sale_date[1] == month_num:
                # Getting all data of this particular date (Month num)
                temp_sale_data = {
                    'customer':str(user_sales.customer_name).title(),
                    'item':f"{(user_sales.order_name).title()} ({user_sales.quantity} {user_sales.qty_weigth})",
                    'date':user_sales.order_date,
                    'date_of_delivery':user_sales.date_of_delivery,
                    'price':user_sales.price,
                    'notes':user_sales.extra_note,
                    'id':user_sales.id,
                } # Temp sale dict 
                user_sale_total_amt += int(user_sales.price) # increamenting sale amount
                user_sale_info.append(temp_sale_data) # Appending all temp dict to final list
        
        # --- Getting Expense Data --- #            
        user_expense_data = Expense.objects.filter(user_id = user) # All exp information from database of user
        # Initializing Variables
        user_expense_info = []
        user_expense_total_amt = 0
        for user_expense in user_expense_data:
            expense_date = user_expense.expense_date.split('-') # Getting month num from exp date
            if expense_date[1] == month_num:
                # Getting all data of this particular date (Month num)
                if user_expense.bill != "":
                    bill = user_expense.bill.url
                else:
                    bill = None
                temp_expense_data = {
                    'item':str(user_expense.expense_name).title(),
                    'qty':f"{user_expense.expense_quantity} {user_expense.qty_unit}",
                    'date':user_expense.expense_date,
                    'price':user_expense.expense_amount,
                    'id':user_expense.id,
                    'notes':user_expense.extra_note, 
                    'bill':bill,                   
                } # Temp exp dict
                user_expense_total_amt += int(user_expense.expense_amount) # increamenting exp amount
                user_expense_info.append(temp_expense_data) # Appending all temp dict to final list
            
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
            
        profile_pfp = user_profile.pfp
        if profile_pfp == "":
            profile_pfp = 0 
        else:    
            profile_pfp = profile_pfp.url 
            
        
        
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
            'is_premium':is_premium,  
            'remaining_days':remaining_days,
            'first_login':user_profile.first_login,  
            'end_date':user_profile.free_end_date,
            'theme':user_profile.theme_selection,
            'premium_ended':premium_ended,
        }        

        if user_profile.first_login == False:
            user_profile_obj = UserProfile.objects.get(user_id=user)
            user_profile_obj.first_login = True
            user_profile_obj.save()
            
        return render(request,"dashboard.html",data)        
    except Exception as e:
        user = request.user
        error_log(error=e,user=user,url=request.build_absolute_uri())
        return redirect('sign_in')

@login_required(login_url=reverse_lazy('sign_in'))
def dashboard_last_month(request):
    try:
        if request.user.is_authenticated:
            if request.session.get_expiry_age() <= 0:
                request.session.set_expiry(30 * 24 * 60 * 60)
        user = request.user    
        user_profile = UserProfile.objects.filter(user_id=user)[0]
        is_premium = user_profile.premium        
        if is_premium == False:
            user_free_date_lst = str(user_profile.free_end_date).split('/')
            user_free_end_date = datetime.date(day=int(user_free_date_lst[0]),month=int(user_free_date_lst[1]),year=int(str("20")+str(user_free_date_lst[2])))
            today = datetime.date.today()
            if today <= user_free_end_date:
                remaining_days = (user_free_end_date - today).days
            else:
                return redirect('plans')
            premium_ended = None
        else:
            premium_is = check_pre_expr(user)
            if premium_is == False:
                premium_ended = True
                return redirect('plans')
            else:
                if premium_is <=5:
                    premium_ended = premium_is
                else:
                    premium_ended = False
            
            remaining_days = None
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
                if user_expense.bill != "":
                    bill = user_expense.bill.url
                else:
                    bill = None
                temp_expense_data = {
                    'item':str(user_expense.expense_name).title(),
                    'qty':f"{user_expense.expense_quantity} {user_expense.qty_unit}",
                    'date':user_expense.expense_date,
                    'price':user_expense.expense_amount,
                    'id':user_expense.id,              
                    'notes':user_expense.extra_note,
                    'bill':bill,

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
            
        profile_pfp = user_profile.pfp
        if profile_pfp == "":
            profile_pfp = 0 
        else:    
            profile_pfp = profile_pfp.url
        is_premium = user_profile.premium
        
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
            'is_premium':is_premium,           
            'remaining_days':remaining_days,
            'first_login':user_profile.first_login,  
            'end_date':user_profile.free_end_date,
            'theme':user_profile.theme_selection, 
            'premium_ended':premium_ended,               
        }
        if user_profile.first_login == False:
            user_profile_obj = UserProfile.objects.get(user_id=user)
            user_profile_obj.first_login = True
        return render(request,"dashboard.html",data)
    
    except Exception as e:
        user = request.user
        error_log(error=e,user=user,url=request.build_absolute_uri())
        return redirect('sign_in')

@login_required(login_url=reverse_lazy('sign_in'))
def dashboard_this_year(request):
    try:
        if request.user.is_authenticated:
            if request.session.get_expiry_age() <= 0:
                request.session.set_expiry(30 * 24 * 60 * 60)
        user = request.user
        user_profile = UserProfile.objects.filter(user_id=user)[0]
        is_premium = user_profile.premium
        if is_premium == False:
            user_free_date_lst = str(user_profile.free_end_date).split('/')
            user_free_end_date = datetime.date(day=int(user_free_date_lst[0]),month=int(user_free_date_lst[1]),year=int(str("20")+str(user_free_date_lst[2])))
            today = datetime.date.today()
            if today <= user_free_end_date:
                remaining_days = (user_free_end_date - today).days
            else:
                return redirect('plans')
            premium_ended = None
        else:
            premium_is = check_pre_expr(user)
            if premium_is == False:
                premium_ended = True
                return redirect('plans')
            else:
                if premium_is <=5:
                    premium_ended = premium_is
                else:
                    premium_ended = False
            
            remaining_days = None
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
                if user_expense.bill != "":
                    bill = user_expense.bill.url
                else:
                    bill = None
                temp_expense_data = {
                    'item':str(user_expense.expense_name).title(),
                    'qty':f"{user_expense.expense_quantity} {user_expense.qty_unit}",
                    'date':user_expense.expense_date,
                    'price':user_expense.expense_amount,
                    'id':user_expense.id,          
                    'notes':user_expense.extra_note,  
                    'bill':bill,    
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
            
        profile_pfp = user_profile.pfp
        if profile_pfp == "":
            profile_pfp = 0 
        else:    
            profile_pfp = profile_pfp.url     
        
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
            'is_premium':is_premium,           
            'remaining_days':remaining_days,
            'first_login':user_profile.first_login,  
            'end_date':user_profile.free_end_date,
            'theme':user_profile.theme_selection,   
            'premium_ended':premium_ended,     
            
        }

        if user_profile.first_login == False:
            user_profile_obj = UserProfile.objects.get(user_id=user)
            user_profile_obj.first_login = True
            user_profile_obj.save()
            
        return render(request,"dashboard.html",data)
    except Exception as e:
        user = request.user
        error_log(error=e,user=user,url=request.build_absolute_uri())
        return redirect('sign_in')

@login_required(login_url=reverse_lazy('sign_in'))
def dashboard_lifetime(request):
    try:
        if request.user.is_authenticated:
            if request.session.get_expiry_age() <= 0:
                request.session.set_expiry(30 * 24 * 60 * 60)
        user = request.user
        user_profile = UserProfile.objects.filter(user_id=user)[0]
        is_premium = user_profile.premium
        if is_premium == False:
            user_free_date_lst = str(user_profile.free_end_date).split('/')
            user_free_end_date = datetime.date(day=int(user_free_date_lst[0]),month=int(user_free_date_lst[1]),year=int(str("20")+str(user_free_date_lst[2])))
            today = datetime.date.today()
            if today <= user_free_end_date:
                remaining_days = (user_free_end_date - today).days
            else:
                return redirect('plans')
            premium_ended = None
        else:
            premium_is = check_pre_expr(user)
            if premium_is == False:
                premium_ended = True
                return redirect('plans')
            else:
                if premium_is <=5:
                    premium_ended = premium_is
                else:
                    premium_ended = False
            
            remaining_days = None
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
            if user_expense.bill != "":
                bill = user_expense.bill.url
            else:
                bill = None
            temp_expense_data = {
                    'item':str(user_expense.expense_name).title(),
                    'qty':f"{user_expense.expense_quantity} {user_expense.qty_unit}",
                    'date':user_expense.expense_date,
                    'price':user_expense.expense_amount,
                    'id':user_expense.id,    
                    'notes':user_expense.extra_note, 
                    'bill':bill,           
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
        
        profile_pfp=user_profile.pfp
        if profile_pfp == "":
            profile_pfp = 0 
        else:    
            profile_pfp = profile_pfp.url 
            
        
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
            'is_premium':is_premium,                       
            'remaining_days':remaining_days,
            'first_login':user_profile.first_login,  
            'end_date':user_profile.free_end_date,  
            'theme':user_profile.theme_selection,
            'premium_ended':premium_ended,
        
        }
        if user_profile.first_login == False:
            user_profile_obj = UserProfile.objects.get(user_id=user)
            user_profile_obj.first_login = True
            user_profile_obj.save()
            
        return render(request,"dashboard.html",data)
    except Exception as e:
        user = request.user
        error_log(error=e,user=user,url=request.build_absolute_uri())
        return redirect('sign_in')

@login_required(login_url=reverse_lazy('sign_in'))
def charts(request):   
    try: 
        if request.user.is_authenticated:
            if request.session.get_expiry_age() <= 0:
                request.session.set_expiry(30 * 24 * 60 * 60)    
        user = request.user
        user_profile = UserProfile.objects.filter(user_id=user)[0]
        is_premium = user_profile.premium
        if is_premium == False:
            user_free_date_lst = str(user_profile.free_end_date).split('/')
            user_free_end_date = datetime.date(day=int(user_free_date_lst[0]),month=int(user_free_date_lst[1]),year=int(str("20")+str(user_free_date_lst[2])))
            today = datetime.date.today()
            if today <= user_free_end_date:
                remaining_days = (user_free_end_date - today).days
            else:
                return redirect('plans')
            premium_ended = None
        else:
            premium_is = check_pre_expr(user)
            if premium_is == False:
                premium_ended = True
                return redirect('plans')
            else:
                if premium_is <=5:
                    premium_ended = premium_is
                else:
                    premium_ended = False
            
            remaining_days = None
        today = datetime.datetime.now()
        st_date = (today-datetime.timedelta(days=7))
        # Income data
        user_sale_data = Sales.objects.filter(user_id=user,order_date__gte=st_date)
        sale_data=[]
        total_sale = 0
        for i in range(7):
            st_date_obj_sale = today-datetime.timedelta(days=i)
            st_dates_sale= st_date_obj_sale.strftime("%Y-%m-%d")           
            st_date_sale_data = user_sale_data.filter(order_date=st_dates_sale)
            tot_amt_sale = 0
            for sale_amt in st_date_sale_data:
                tot_amt_sale += int(sale_amt.price)
            total_sale+=tot_amt_sale
            sale_data.append({'date':st_date_obj_sale.strftime("%d/%m/%y"),'amt':tot_amt_sale,})
            
        # Expense data
        user_exp_data = Expense.objects.filter(user_id=user,expense_date__gte=st_date)
        exp_data = []
        total_exp=0
        for i in range(7):
            st_date_obj_exp = today-datetime.timedelta(days=i)
            st_dates_exp = st_date_obj_exp.strftime("%Y-%m-%d")
            st_date_exp_data = user_exp_data.filter(expense_date = st_dates_exp)
            tot_amt_exp = 0
            for exp_amt in st_date_exp_data:
                tot_amt_exp+=int(exp_amt.expense_amount)
            total_exp+=tot_amt_exp
            exp_data.append({'date':st_date_obj_exp.strftime("%d/%m/%y"),'amt':tot_amt_exp,})
        
        # Category data
        user_category = Category.objects.filter(user_id=user)
        st_date_cate = today.replace(day=1)
        curr_month_category_data = Sales.objects.filter(user_id=user,order_date__gte=st_date_cate)        
        category_data = []       
        if len(user_category) == 0:
            category_data = None
        else:
            for category in user_category:
                category_user_datas = curr_month_category_data.filter(category=category.category)               
                tot_amt_cate = 0
                for category_user_data in category_user_datas:
                    tot_amt_cate+=int(category_user_data.price)                                                    
                category_data.append({'category':category.category,'amt':tot_amt_cate})    
        
        profile_pfp = user_profile.pfp
        if profile_pfp == "":
            profile_pfp = 0 
        else:    
            profile_pfp = profile_pfp.url 
                    
            
            
        data={
            'tab':4,
            'user':user,
            'profile_pfp':profile_pfp,
            'sale_data':sale_data,
            'category_data':category_data,
            'exp_data':exp_data,
            'category_data':category_data,
            'total_sale':"{:,.0f}".format(total_sale),
            'total_exp':"{:,.0f}".format(total_exp),
            'p_letter':str(user.first_name)[0].lower(),  
            'is_premium':is_premium,           
            'remaining_days':remaining_days,
            'theme':user_profile.theme_selection,
            'premium_ended':premium_ended,
            
            
        }
        return render(request,'charts.html',data)
    except Exception as e:
        user = request.user
        error_log(error=e,user=user,url=request.build_absolute_uri())
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
            
            user_profile = UserProfile.objects.filter(user_id=user)[0]
            profile_pfp = user_profile.pfp
            if profile_pfp == "":
                profile_pfp = 0 
            else:    
                profile_pfp = profile_pfp.url
                
            is_premium = user_profile.premium
            if is_premium == False:
                user_free_date_lst = str(user_profile.free_end_date).split('/')
                user_free_end_date = datetime.date(day=int(user_free_date_lst[0]),month=int(user_free_date_lst[1]),year=int(str("20")+str(user_free_date_lst[2])))
                today = datetime.date.today()
                if today <= user_free_end_date:
                    remaining_days = (user_free_end_date - today).days
                else:
                    return redirect('plans')
                premium_ended = None
            else:
                premium_is = check_pre_expr(user)
                if premium_is == False:
                    premium_ended = True
                    return redirect('plans')
                else:
                    if premium_is <=5:
                        premium_ended = premium_is
                    else:
                        premium_ended = False
                
                remaining_days = None
            
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
                'is_premium':is_premium,           
                'remaining_days':remaining_days,
                'theme':user_profile.theme_selection,
                'premium_ended':premium_ended,

            }       
            request.session['sale_id'] = None
            return render(request,'sale_edit.html',data)  
    except Exception as e:
        user = request.user
        error_log(error=e,user=user,url=request.build_absolute_uri())
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
                
        user_profile = UserProfile.objects.filter(user_id=user)[0]
        profile_pfp = user_profile.pfp
        if profile_pfp == "":
            profile_pfp = 0 
        else:    
            profile_pfp = profile_pfp.url 
            
        is_premium = user_profile.premium    
        if is_premium == False:
            user_free_date_lst = str(user_profile.free_end_date).split('/')
            user_free_end_date = datetime.date(day=int(user_free_date_lst[0]),month=int(user_free_date_lst[1]),year=int(str("20")+str(user_free_date_lst[2])))
            today = datetime.date.today()
            if today <= user_free_end_date:
                remaining_days = (user_free_end_date - today).days
            else:
                return redirect('plans')
            premium_ended = None
        else:
            premium_is = check_pre_expr(user)
            if premium_is == False:
                premium_ended = True
                return redirect('plans')
            else:
                if premium_is <=5:
                    premium_ended = premium_is
                else:
                    premium_ended = False
            
            remaining_days = None
        
        category_data = Category.objects.filter(user_id = user)
        data = {
            'tab':2,
            'sale':sale_add,
            'p_letter':str(user.first_name)[0].lower(),    
            'profile_pfp':profile_pfp,       
            'user':user,
            'category_data':category_data,
            'category_len':len(category_data),
            'is_premium':is_premium,           
            'remaining_days':remaining_days,
            'theme':user_profile.theme_selection,
            'premium_ended':premium_ended,
                
        }
        return render(request,"sale_adder.html",data)
    except Exception as e:
        user = request.user
        error_log(error=e,user=user,url=request.build_absolute_uri())
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
            
            user_profile = UserProfile.objects.filter(user_id=user)[0]
            profile_pfp = user_profile.pfp
            if profile_pfp == "":
                profile_pfp = 0 
            else:    
                profile_pfp = profile_pfp.url
                
            is_premium = user_profile.premium
            if is_premium == False:
                user_free_date_lst = str(user_profile.free_end_date).split('/')
                user_free_end_date = datetime.date(day=int(user_free_date_lst[0]),month=int(user_free_date_lst[1]),year=int(str("20")+str(user_free_date_lst[2])))
                today = datetime.date.today()
                if today <= user_free_end_date:
                    remaining_days = (user_free_end_date - today).days
                else:
                    return redirect('plans')
                premium_ended = None
            else:
                premium_is = check_pre_expr(user)
                if premium_is == False:
                    premium_ended = True
                    return redirect('plans')
                else:
                    if premium_is <=5:
                        premium_ended = premium_is
                    else:
                        premium_ended = False
                
                remaining_days = None
            
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
                'is_premium':is_premium,           
                'remaining_days':remaining_days,
                'theme':user_profile.theme_selection,
                'premium_ended':premium_ended,

            }       
            request.session['expense_id'] = None
            return render(request,'expense_edit.html',data)   
    except Exception as e:
        user = request.user
        error_log(error=e,user=user,url=request.build_absolute_uri())
        return redirect('dashboard')
    
@login_required(login_url=reverse_lazy('sign_in'))
def expense_adder(request):
    try:
        expense_add = None
        user = request.user
        if request.method == 'POST': 
            try:   
                bill=request.FILES.get('bill')   
                if(bill):
                    img = Image.open(bill).convert('RGB')
                    # img = img.convert('RGB')
                    img = img.reduce(factor=2)
                    buffer = BytesIO()
                    img.save(buffer, format='JPEG')
                    buffer.seek(0)
                    file = InMemoryUploadedFile(
                        buffer,
                        'ImageField',
                        f"{bill.name.split('.')[0]}_compressed.jpg",
                        'image/jpeg',
                        buffer.getbuffer().nbytes,
                        None
                    )
                    add_expense = Expense(user_id = user,
                                            expense_name = request.POST.get('expense_name'),
                                            expense_amount = request.POST.get('expense_amount'),
                                            expense_quantity =request.POST.get('expense_quantity'),
                                            qty_unit = request.POST.get('qty_unit'),
                                            extra_note = request.POST.get('extra_note'),
                                            expense_date = request.POST.get('expense_date'),
                                            bill=file,
                                    )
                else:
                    add_expense = Expense(user_id = user,
                                            expense_name = request.POST.get('expense_name'),
                                            expense_amount = request.POST.get('expense_amount'),
                                            expense_quantity =request.POST.get('expense_quantity'),
                                            qty_unit = request.POST.get('qty_unit'),
                                            extra_note = request.POST.get('extra_note'),
                                            expense_date = request.POST.get('expense_date'),
                                            bill=None,
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
        user_profile = UserProfile.objects.filter(user_id=user)[0]
        profile_pfp = user_profile.pfp
        if profile_pfp == "":
            profile_pfp = 0 
        else:    
            profile_pfp = profile_pfp.url     
            
        is_premium = user_profile.premium       
        if is_premium == False:
            user_free_date_lst = str(user_profile.free_end_date).split('/')
            user_free_end_date = datetime.date(day=int(user_free_date_lst[0]),month=int(user_free_date_lst[1]),year=int(str("20")+str(user_free_date_lst[2])))
            today = datetime.date.today()
            if today <= user_free_end_date:
                remaining_days = (user_free_end_date - today).days
            else:
                return redirect('plans')
            premium_ended = None
        else:
            premium_is = check_pre_expr(user)
            if premium_is == False:
                premium_ended = True
                return redirect('plans')
            else:
                if premium_is <=5:
                    premium_ended = premium_is
                else:
                    premium_ended = False
            
            remaining_days = None
        user_exp = Expense.objects.filter(user_id = user)
        if len(user_exp)>0:            
            frequent_expenses = user_exp.values('expense_name').annotate(count=Count('expense_name'))
            frequent_expenses = frequent_expenses.order_by('-count')
            frequent_expenses = frequent_expenses[:2]                      
            frequent_expenses_data = []
            for frequent_exp in frequent_expenses:
                expense_name=frequent_exp['expense_name']              
                expense_data = user_exp.filter(expense_name=expense_name).values('expense_name','expense_amount','expense_quantity','qty_unit','extra_note')                            
                frequent_expenses_data.append(expense_data[len(expense_data)-1])
                
        else:
            frequent_expenses_data = None         
            
        data = {
            'tab':3,
            'expense':expense_add,
            'p_letter':str(user.first_name)[0].lower(),  
            'profile_pfp':profile_pfp,  
            'frequent_expenses_data':frequent_expenses_data,  
            'is_premium':is_premium,   
            'remaining_days':remaining_days,
            'theme':user_profile.theme_selection,   
            'premium_ended':premium_ended,         
                
        }
        return render(request,"expense_adder.html",data)
    except Exception as e:
        user = request.user
        error_log(error=e,user=user,url=request.build_absolute_uri())
        return redirect('dashboard')
    
@login_required(login_url=reverse_lazy('sign_in'))
def profile(request):
    try:
        user = request.user
        user_profile=UserProfile.objects.get(user_id = user)
        if request.method == 'POST':
            if request.POST.get('pfp_changed') == 'True':            
                try:
                    image = request.FILES.get('pfp')
                    img = Image.open(image).convert('RGB')
                    # img = img.convert('RGB')
                    img = img.reduce(factor=2)
                    buffer = BytesIO()
                    img.save(buffer, format='JPEG')
                    buffer.seek(0)
                    file = InMemoryUploadedFile(
                        buffer,
                        'ImageField',
                        f"{image.name.split('.')[0]}_compressed.jpg",
                        'image/jpeg',
                        buffer.getbuffer().nbytes,
                        None
                    )
                    user_profile.pfp.save(file.name, file, save=True)     
                except:
                    pass          
            request.user.first_name = request.POST.get('first_name')
            request.user.last_name = request.POST.get('last_name')
            user.save()            
            # user_profile=UserProfile.objects.get(user_id = user)
            user_profile.first_name = request.POST.get('first_name')
            user_profile.last_name = request.POST.get('last_name')
            user_profile.save()
            
        profile_pfp = user_profile.pfp
        if profile_pfp == "":
            profile_pfp = 0 
        else:    
            profile_pfp = profile_pfp.url
            
        is_premium = user_profile.premium
        if is_premium == False:
            user_free_date_lst = str(user_profile.free_end_date).split('/')
            user_free_end_date = datetime.date(day=int(user_free_date_lst[0]),month=int(user_free_date_lst[1]),year=int(str("20")+str(user_free_date_lst[2])))
            today = datetime.date.today()
            if today <= user_free_end_date:
                remaining_days = (user_free_end_date - today).days
            else:
                return redirect('plans')
            premium_ended = None
            start_date = None
            end_date = None
        else:
            premium_is = check_pre_expr(user)
            if premium_is == False:
                premium_ended = True
                return redirect('plans')
            else:
                if premium_is <=5:
                    premium_ended = premium_is
                else:
                    premium_ended = False                    
            
            remaining_days = None
            start_date = str(user_profile.premium_start_date).split('/')
            start_date = datetime.date(day=int(start_date[0]),month=int(start_date[1]),year=int(start_date[2])).strftime("%d %B, %Y")
            end_date = str(user_profile.premium_end_date).split('/')
            end_date = datetime.date(day=int(end_date[0]),month=int(end_date[1]),year=int(end_date[2])).strftime("%d %B, %Y")
            
        data = {
            'first_name':request.user.first_name,
            'last_name':request.user.last_name,
            'email':request.user.email,
            'p_letter':str(user.first_name)[0].lower(), 
            'profile_pfp':profile_pfp,    
            'tab':5,   
            'is_premium':is_premium,           
            'remaining_days':remaining_days,
            'theme':user_profile.theme_selection, 
            'premium_ended':premium_ended, 
            'start_date':start_date,
            'end_date':end_date,
            'plan':f'{user_profile.premium_month_plan} Days'
                
        }
        return render(request,'profile.html',data)
    except Exception as e:
        user = request.user
        error_log(error=e,user=user,url=request.build_absolute_uri())
        return redirect('dashboard')

@login_required(login_url=reverse_lazy('sign_in'))
def settings(request):
    try:
        user = request.user
        user_profile = UserProfile.objects.filter(user_id=user)[0]
        if request.method == 'POST':
            user_obj = UserProfile.objects.get(user_id=user)
            user_obj.first_view = request.POST.get('first_view')
            user_obj.theme_selection = request.POST.get('theme')
            user_obj.save()
            return redirect('settings')
            
        user_view = user_profile.first_view
        profile_pfp = user_profile.pfp
        is_premium = user_profile.premium
        if is_premium == False:
            user_free_date_lst = str(user_profile.free_end_date).split('/')
            user_free_end_date = datetime.date(day=int(user_free_date_lst[0]),month=int(user_free_date_lst[1]),year=int(str("20")+str(user_free_date_lst[2])))
            today = datetime.date.today()
            if today <= user_free_end_date:
                remaining_days = (user_free_end_date - today).days
            else:
                return redirect('plans')
            premium_ended = None    
                    
        else:
            premium_is = check_pre_expr(user)
            if premium_is == False:
                premium_ended = True
                return redirect('plans')
            else:
                if premium_is <=5:
                    premium_ended = premium_is
                else:
                    premium_ended = False                    
            remaining_days = None
                        
        if profile_pfp == "":
            profile_pfp = 0 
        else:    
            profile_pfp = profile_pfp.url 
        data={
            'p_letter':str(user.first_name)[0].lower(), 
            'profile_pfp':profile_pfp,    
            'tab':6,
            'user_view':user_view,   
            'is_premium':is_premium,  
            'remaining_days':remaining_days,
            'theme':user_profile.theme_selection,
            'premium_ended':premium_ended,
            
            
        }
        return render(request,'settings.html',data)
    except Exception as e:
        user = request.user
        error_log(error=e,user=user,url=request.build_absolute_uri())
        return redirect('dashboard')    

## ---- API FUNCTIONS ---- ##
def api_add_category(request):
    if request.method == 'POST':
        #(needs to be change)
        category = request.POST.get('category')
        user_id = request.POST.get('user_id')
        category_add = Category(category=category,user_id=user_id)
        category_add.save()
        return JsonResponse({'success': True})

## ---- EXTRA FUNCTIONS ---- ##
def extra_code():
#Extras
        # Saving all user joining dates to userprofile database
        # users = User.objects.all()
        # for user__ in users:
        #     user_obj_pro = UserProfile.objects.get(user_id=user__)
        #     user_obj_pro.join_date = datetime.date(year=int(str(user__.date_joined.date()).split("-")[0]),month=int(str(user__.date_joined.date()).split("-")[1]),day=int(str(user__.date_joined.date()).split("-")[2])).strftime("%d/%m/%y")
            ## Ending date ##
            # user_join_date_extra = datetime.date(year=int(str(user__.date_joined.date()).split("-")[0]),month=int(str(user__.date_joined.date()).split("-")[1]),day=int(str(user__.date_joined.date()).split("-")[2]))
            # user_free_end_date = user_join_date_extra+datetime.timedelta(days=14)
            # user_obj_pro.free_end_date = user_free_end_date.strftime("%d/%m/%y")

        #     user_obj_pro.save()
             
    pass  
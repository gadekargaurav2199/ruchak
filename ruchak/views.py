import re
from django.shortcuts import render
from django.http import HttpResponse

from django.contrib import messages
from django.shortcuts import redirect
import hashlib

from requests import session

from myhotel.models import User, inquiry



def home(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        
        if not email or not password:
            messages.error(request, 'Please provide both email and password.')
            return redirect("/")
        
        # Hash the password with SHA-256
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Check if the user exists
        try:
            user = User.objects.get(email=email, password=hashed_password)
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password')
            return redirect('/')  # Redirect back to login page with error message
        except Exception as e:
            messages.error(request, 'Oops! Something Wrong')
            return redirect('/')  # Redirect back to login page with error message
       
        # If user exists and password matches, create session and redirect to home page
        request.session['user_id'] = user.pk
        request.session['hotel'] = user.hotel_name
        request.session['contact1'] = user.mobile_number
        request.session['contact2'] = user.alternate_number
        messages.success(request, 'Login successful')
        return redirect('/myhotel/')  # Redirect to home page or any other desired page

    table_count = 21
    return render(request, 'home.html', {'table_count': table_count})



def register_me(request):
    if 'admin' not in request.session:
        return redirect('/')
    if request.method == 'POST':
        try:
            # Retrieve form data
            hotel_name = request.POST.get('hotelName')
            address = request.POST.get('address')
            mobile_number = request.POST.get('mobileNumber')
            alternate_number = request.POST.get('alternateNumber')
            password = request.POST.get('password')
            valid_upto = request.POST.get('validUpto')
            payment = request.POST.get('payment')
            details = request.POST.get('details')
            # Encrypting the password using SHA-256 algorithm
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            # Create the user object with the hashed password
            try:
                is_exists=User.objects.get(email=mobile_number)
                messages.error(request,"Record Already Available Please Login Directly")
                return redirect("/")
            except:
                pass

            user = User.objects.create(
                hotel_name=hotel_name,
                address=address,
                mobile_number=mobile_number,
                alternate_number=alternate_number,
                email=mobile_number,
                password=hashed_password,
                valid_upto=valid_upto,
                payment=payment,
                details=details
            )
            try:
                user.save()
                messages.success(request, 'User created successfully!')
            except:
                messages.error(request,"Oops Something Went to Wrong!")
            
        except Exception as e:
            print(e)
            messages.error(request, e)
    
        return redirect("/register_me/")

    users_list=User.objects.all()

    return render(request, 'register_me.html',{'users':users_list})
def superuser(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        
        if not email or not password:
            messages.error(request, 'Please provide both email and password.')
            return redirect("/")
        
        # Hash the password with SHA-256
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Check if the user exists
        try:
            user = User.objects.get(email=email, password=hashed_password, is_admin=True)
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password')
            return redirect('/')  # Redirect back to login page with error message
        except Exception as e:
            messages.error(request, 'Oops! Something Wrong')
            return redirect('/')  # Redirect back to login page with error message
       
        # If user exists and password matches, create session and redirect to home page
        request.session['user_id'] = user.pk
        request.session['hotel'] = user.hotel_name
        request.session['contact1'] = user.mobile_number
        request.session['contact2'] = user.alternate_number
        request.session['admin'] = True
        messages.success(request, 'Login successful')
        return redirect('/register_me/')  # Redirect to home page or any other desired page
    table_count=21
    return render(request,'superuser.html' ,{'table_count':table_count})




def inquiry_def(request):
    if request.method == 'POST':
        try:
            if request.session.get('count')==3:
                messages.error(request,"Maximum Inquiry Limit Will Crossed")
                return redirect("/")
            mobile_number_pattern = r'^\d{10}$'
            mobile = request.POST.get('inquiry')
            if re.match(mobile_number_pattern, mobile):
                print("Valid mobile number")
                inquiry_model=inquiry()
                inquiry_model.mobile=mobile
                inquiry_model.save()
                request.session['count'] = request.session.get('count', 0) + 1
                messages.success(request,"Inquiry Generated Successfylly! Our team Call You After Few Minutes!")
            else:
                messages.error(request,"Please Enter Valid Mobile Number")
        except Exception as e:
            print(e)
            messages.error(request,"Oops! Please Try Again")

    return redirect("/")
def logout(request):
    request.session.flush()
    return redirect("/")
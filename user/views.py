from django.shortcuts import render,redirect,reverse,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from django.contrib.auth.models import User
from cart.models import  Cart
from .models import UserProfile

def user_login(request):
    #if alredy logged in go to home page
    if request.user.is_authenticated:
        return redirect(reverse('home'))

    if request.method == 'POST':
        #get the login info from form
        username = request.POST['username']
        password = request.POST['pass1']     

        #check the info provided is in the database
        user = authenticate(username=username, password=password)
        if user:
            #user exists, aithorizing the user
            login(request,user)

            #set the user's num cart
            try:
                cart = user.cart.get()
            except:
                cart = None 
            if cart:
                num_items = cart.getItems()
                request.session["num_cart"] = str(num_items)
        
            
            #check if the user is admin
            if user.is_superuser:
                #redirect to the admin page
                return redirect('/admin')
            
            #check if there is next_url
            next_url = request.POST['next']
            if next_url != 'None':
                #redirect to the post url
                return redirect(next_url)    
            #redirect to the home page
            return redirect(reverse('home'))
        else:
            #user not found, show error 
            error_message = "Bummer! wrong credentials".format(username)
            return render(request, 'login.html',{'error':error_message})  
            

    #show the login page
    next_url = request.GET.get('next')
    return render(request, 'login.html',context={'next':next_url})

def user_register(request):
    #if alredy logged in go to home page
    if request.user.is_authenticated:
        return redirect(reverse('home'))

    #store the error message if any
    error_message = ''

    if request.method == 'POST':
        #getting the data from the form
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        phone = request.POST['phone']
        address = request.POST['address']
        photo = request.FILES['avatar']


        #validate form
        #check password matches
        if pass1 != pass2:
            error_message = "Password did't matched"
            return render(request, 'register.html',{'error':error_message})

        #check username exists
        if User.objects.filter(username=username).count() > 0:
            error_message = "User {} already exists. Please try another one".format(username)
            return render(request, 'register.html',{'error':error_message})
        
        
        #add the user info to the databse
        user = User.objects.create_user(username=username, password=pass1)
        UserProfile.objects.create(
            user=user,
            email=email,
            name=name,
            address=address,
            phone=phone,
            photo=photo,
        )
        
        #redirecct to the login page
        return redirect(reverse('login'))

    #show register page to the user    
    return render(request, 'register.html')

def user_logout(request):
    #just logut the user and redirect to the home page
    logout(request)
    return redirect(reverse('home'))

@login_required
def user_profile(request):
    #show user the profile
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request,'user_profile.html',context={"user_profile":user_profile,'title':'profile'})
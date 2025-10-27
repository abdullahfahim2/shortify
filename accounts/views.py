from django.shortcuts import render,redirect,get_object_or_404
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages


def registerview(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            # login(request,user)
            messages.success(request,"Your Account is Created Succesfully!please login with your credentials")
            return redirect('login')
        
        else:
            messages.error(request,'Something Went Wrong , Please Fill All The Fields and try again!')
            return redirect('login')
        
    form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form':form})


def loginview(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request,username=email,password=password)
        if user:
            login(request,user)
            messages.success(request,"You've Successfully Logged into Your Account!")
            return redirect('dashboard')
        
        else:
            messages.error(request,"Invalid Email or Password!Please Try Again.")
            return redirect('login')
        
    return render(request, 'accounts/signin.html', {})
    

def logoutview(request):
    logout(request)
    messages.success(request,"Thanks For Using Our System!")
    return redirect('login')


def dashboardview(request):
    return render(request, 'accounts/dashboard/dashboard.html', {})
    
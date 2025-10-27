from django.shortcuts import render,redirect,get_object_or_404
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def registerview(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.success(request,"Your Account is Created Succesfully!")
            return redirect('dashboard')
        
        else:
            messages.error(request,'Something Went Wrong , Please Fill All The Fields and try again!')        
    form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form':form})


def loginview(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
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
    
@login_required
def logoutview(request):
    logout(request)
    messages.success(request,"Thanks For Using Our System!")
    return redirect('login')

@login_required
def dashboardview(request):
    return render(request, 'accounts/dashboard/dashboard.html', {})


@login_required
def profileview(request):
    return render(request , 'accounts/dashboard/profile.html')
    

@login_required
def analyticsview(request):
    return render(request, 'accounts/dashboard/analytics.html', {})


@login_required
def managelinksview(request):
    return render(request, 'accounts/dashboard/managelinks.html', {})
    
    
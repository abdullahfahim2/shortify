from django.shortcuts import render,redirect,get_object_or_404
from .forms import CustomUserCreationForm
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from core.models import UserLink,ClickEvent
from django.db.models import Q, Sum



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
    """Main dashboard overview with link stats."""
    total_links = UserLink.objects.filter(user=request.user).count()
    total_clicks = ClickEvent.objects.filter(link__user=request.user).count()
    active_links = UserLink.objects.filter(user=request.user, is_active=True).count()
    expired_links = UserLink.objects.filter(user=request.user, expire_at__lt=timezone.now()).count()
    recent_links = UserLink.objects.filter(user=request.user).order_by('-created_at')[:5]

    context = {
        'total_links': total_links,
        'total_clicks': total_clicks,
        'active_links': active_links,
        'expired_links': expired_links,
        'recent_links': recent_links,
    }
    return render(request, 'accounts/dashboard/dashboard.html', context)

@login_required
def analyticsview(request):
    links = UserLink.objects.filter(user=request.user).order_by('-created_at')
    total_clicks = ClickEvent.objects.filter(link__user=request.user).count()
    unique_visitors = ClickEvent.objects.filter(link__user=request.user).values('ip_address').distinct().count()
    avg_ctr = round((total_clicks / links.count()) * 100, 2) if links.exists() else 0

    context = {
        'links': links,
        'total_clicks': total_clicks,
        'unique_visitors': unique_visitors,
        'avg_ctr': avg_ctr,
    }
    return render(request, 'accounts/dashboard/analytics.html', context)


@login_required
def managelinksview(request):
    """Display and manage all user-created links."""
    user = request.user
    query = request.GET.get("q", "").strip()
    links = UserLink.objects.filter(user=user).order_by("-created_at")

    # ✅ Search logic
    if query:
        links = links.filter(
            Q(original_url__icontains=query) |
            Q(custom_alias__icontains=query) |
            Q(short_code__icontains=query)
        )

    # ✅ Calculate stats
    total_links = links.count()
    total_clicks = links.aggregate(total=Sum("click_count"))["total"] or 0
    active_links = links.filter(is_active=True).count()
    inactive_links = total_links - active_links

    # ✅ Handle link deletion
    if request.method == "POST":
        delete_id = request.POST.get("delete_id")
        if delete_id:
            link = get_object_or_404(UserLink, id=delete_id, user=user)
            link.delete()
            messages.success(request, "Link deleted successfully.")
            return redirect("managelinks")

    context = {
        "links": links,
        "query": query,
        "total_links": total_links,
        "total_clicks": total_clicks,
        "active_links": active_links,
        "inactive_links": inactive_links,
    }

    return render(request, "accounts/dashboard/managelinks.html", context)

from django.shortcuts import render, redirect
from django.utils import timezone
from .models import AnonymousShortURL
from .models import UserLink 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import timedelta
from django.http import HttpResponseForbidden
from .models import *

# Landing page view with URL shortener form
def landingpageview(request):
    short_url = None  # To display generated short link

    if request.method == 'POST':
        original_url = request.POST.get('original_url')

        if original_url:
            # safely find if the link already exists
            short_link = AnonymousShortURL.objects.filter(original_url=original_url).first()
            if short_link:
                short_url = request.build_absolute_uri(short_link.short_url())
            else:
                # Create new anonymous short URL
                short_link = AnonymousShortURL.objects.create(original_url=original_url)
                short_url = request.build_absolute_uri(short_link.short_url())

    return render(request, 'core/index.html', {'short_url': short_url})



@login_required
def createlink(request):
    created_link = None

    if request.method == "POST":
        original_url = request.POST.get("destination-url")
        custom_alias = request.POST.get("custom-alias")
        link_title = request.POST.get("link-title")
        generate_qr = request.POST.get("qr-code")

        if not original_url:
            messages.error(request, "Destination URL is required.")
            return redirect("createlink")

        # Check alias conflict
        if custom_alias and UserLink.objects.filter(short_code=custom_alias).exists():
            messages.error(request, "This custom alias is already in use.")
            return redirect("createlink")

        # Create link
        link = UserLink.objects.create(
            user=request.user,
            original_url=original_url,
            short_code=custom_alias or "",
            expire_at=timezone.now() + timedelta(days=180),
        )

        # Generate QR if checked
        if generate_qr:
            link.generate_qr_code()
            link.save()

        created_link = request.build_absolute_uri(link.short_url())
        messages.success(request, "Short link created successfully!")

        return render(
            request,
            "core//create_link.html",
            {"created_link": created_link},
        )

    return render(request, "core//create_link.html")


# Redirect Logic for short URLs
def redirect_short_url(request, short_code):
    """Redirect user to original URL for any short link."""
    link = None
    is_user_link = False

    # Try to find in UserLink first
    try:
        link = UserLink.objects.get(short_code=short_code)
        is_user_link = True
    except UserLink.DoesNotExist:
        # Try anonymous short link
        link = AnonymousShortURL.objects.filter(short_code=short_code).first()

    if not link:
        messages.error(request, "Invalid or expired short link.")
        return redirect("createlink")

    # Check expiry
    if link.expire_at and link.expire_at < timezone.now():
        messages.error(request, "This short link has expired.")
        return redirect("createlink")

    # Check active status (for user links)
    if is_user_link and not link.is_active:
        return HttpResponseForbidden("This link is inactive.")

    # Update click count
    link.click_count = getattr(link, "click_count", 0) + 1
    link.save(update_fields=["click_count"])

    # Log ClickEvent for user links only
    if is_user_link:
        ip = get_client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "")
        referrer = request.META.get("HTTP_REFERER", "")

        ClickEvent.objects.create(
            link=link,
            ip_address=ip,
            user_agent=user_agent,
            referrer=referrer,
        )

    # Redirect to original URL
    return redirect(link.original_url)


# Helper to get real client IP
def get_client_ip(request):
    """Extract client IP address safely."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip

    
    

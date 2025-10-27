from django.shortcuts import render, redirect
from django.utils import timezone
from .models import AnonymousShortURL

# Landing page view with URL shortener form
def landingpageview(request):
    short_url = None  # To display generated short link

    if request.method == 'POST':
        original_url = request.POST.get('original_url')

        if original_url:
            # finding if the link already listed
            short_link = AnonymousShortURL.objects.get(original_url=original_url)
            if short_link:
                short_url = request.build_absolute_uri(short_link.short_url())
            else:
                # Create anonymous short URL
                short_link = AnonymousShortURL.objects.create(original_url=original_url)
                short_url = request.build_absolute_uri(short_link.short_url())  # Full URL

    return render(request, 'core/index.html', {'short_url': short_url})


# Redirect view for short URLs
def redirect_to_original(request, short_code):
    try:
        # Get the short link
        short_link = AnonymousShortURL.objects.get(short_code=short_code)

        # Check if link is expired
        if short_link.expire_at < timezone.now():
            return render(request, 'core/expired.html') 
        # Increment click count
        short_link.click_count += 1
        short_link.save()

        return redirect(short_link.original_url)

    except AnonymousShortURL.DoesNotExist:
        return render(request, 'core/404.html')  # You can create a 404 page


# @login_required
# def create_linkview(request):
#     return render(request, 'core/create_link.html', {})
    
    

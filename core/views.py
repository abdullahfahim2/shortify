from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def landingpageview(request):
    return render(request, 'core/index.html', {})

@login_required
def create_linkview(request):
    return render(request, 'core/create_link.html', {})
    
    

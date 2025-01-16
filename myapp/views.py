from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserCreationForm

from django.http import HttpResponse

def manage_users_view(request):
    return HttpResponse("This is the Manage Users page.")

def add_role_view(request):
    return HttpResponse("This is the Add Role page.")




def add_user_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')  # Redirect to admin panel or another view
    else:
        form = UserCreationForm()

    return render(request, 'admin_panel.html', {'form': form})


def category_view(request):
    """Render the dynamic category view with a dynamic navbar"""
    navbar_links = []

    # Dynamically add links based on user input or any logic you have
    if request.user.is_authenticated:
        navbar_links.append({'name': 'Dashboard', 'url': '/admin-panel/'})
        if request.user.userprofile.role.name == 'Admin':
            navbar_links.append({'name': 'Manage Users', 'url': '/manage-users/'})
        else:
            navbar_links.append({'name': 'Profile', 'url': '/profile/'})
    
    return render(request, 'navbar.html', {'navbar_links': navbar_links})

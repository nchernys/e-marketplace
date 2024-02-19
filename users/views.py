from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from new_shop.models import AddCart


def login_view(request):

     return render(request, 'registration/login.html')

def register(request):
    
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = RegistrationForm()

    return render(request, 'registration/user_register.html', {'form': form})



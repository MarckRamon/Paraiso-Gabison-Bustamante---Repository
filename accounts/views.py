from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import AdminRegistrationForm, AdminLoginForm
from .models import Admin

def register(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after successful registration
    else:
        form = AdminRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    form = AdminLoginForm()

    if request.method == "POST":
        form = AdminLoginForm(request.POST)
        print(form.is_valid())
       # if form.is_valid():
        try:
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('inventory/dashboard.html')
            else:
                form.add_error(None, "Invalid username or password") 
        except Exception as e:
            print(e)
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    return render(request, 'inventory/dashboard.html')

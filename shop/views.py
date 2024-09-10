from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Book

# Create your views here.
def home(request):
    mybooks = Book.objects.all().values()
    template = loader.get_template('home.html')
    context = {'mybooks': mybooks}
    return HttpResponse(template.render(context, request))

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Set the email field for the user
            user.email = request.POST['email']
            user.save()
            login(request, user)
            return redirect('home')  # Redirect to home after signup
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            # Get the user by email
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home after login
        except User.DoesNotExist:
            pass  # Handle invalid login attempt (optional: add a message)
    return render(request, 'login.html')

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            HttpResponse('\'Successful login\'')
        else:
            HttpResponse('\'Disabled account\'')
    else:
        HttpResponse('\'Invalid login\'')

def logout(request):
    logout(request)
    return HttpResponse('\'Successful logout\'')

def signup(request):
    pass

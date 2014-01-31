from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
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
    print request.POST
    username = request.POST['username']
    password = request.POST['password1']
    try:
        email = request.POST['email']
    except KeyError:
        email = ""

    try:
        User.objects.get(username=username)
    except User.DoesNotExist:
        print "Should make a thing"
        user = User.objects.create_user(username,email,password)
        user.save()
        return HttpResponse('\'Made User\'')
    return HttpResponse('\'Failed to made a user\'')

        
        

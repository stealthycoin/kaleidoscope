from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as dj_login
from django.contrib.auth import logout as dj_logout
from django.contrib.auth.models import User
from django.http import HttpResponse

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            dj_login(request, user)
            return HttpResponse('\'Successful login\'')
        else:
            return HttpResponse('\'Disabled account\'')
    else:
        return HttpResponse('\'Invalid login\'')

def logout(request):
    dj_logout(request)
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

        
        

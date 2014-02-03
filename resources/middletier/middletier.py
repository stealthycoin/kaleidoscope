from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as dj_login
from django.contrib.auth import logout as dj_logout
from django.contrib.auth.models import User
from django.http import HttpResponse



def permissionsCheck(request, loggedIn, groups):
    """checks to see that the user has the required permissions to do something"""

    if loggedIn == False:
        #we dont even care if the user is logged in, so yes they have access
        return True
    
    user = request.user

    if not user.is_authenticated():
        #user is not logged in so return false
        return False

    #user is logged in but we need to check groups
    if groups == '':
        return True #no group requirements

    for group in groups.split(" "):
        print group
        if user.groups.filter(name=group).count() == 0:
            return False #they aren't in a required group
        
    return True


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

        
        

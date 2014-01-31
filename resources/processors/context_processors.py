from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.template.loader import render_to_string
from django.template import RequestContext

def loginForm(request):    
    try:
        csrf_token_value = request.COOKIES['csrftoken']
    except KeyError:
        csrf_token_value = "dunno"
    return {
        'login' : render_to_string('userforms.html',\
                                   { 'data' : AuthenticationForm().as_table(),\
                                     'dst' : 'login',\
                                     'csrf_token_value' : csrf_token_value })
    }
    
def signupForm(request):
    try:
        csrf_token_value = request.COOKIES['csrftoken']
    except KeyError:
        csrf_token_value = "dunno"
    return {
        'signup' : render_to_string('userforms.html',\
                                    { 'data' : UserCreationForm().as_table(),\
                                      'dst' : 'signup',\
                                      'csrf_token_value' : csrf_token_value })
    }
    
def logoutForm(request):
    try:
        csrf_token_value = request.COOKIES['csrftoken']
    except KeyError:
        csrf_token_value = "dunno"
    return {
        'logout' : render_to_string('userforms.html',\
                                    { 'data' : '<tr><td><input type="submit" value="Logout" /></td></tr>',\
                                      'dst' : 'logout',\
                                      'csrf_token_value' : csrf_token_value })
    }
    

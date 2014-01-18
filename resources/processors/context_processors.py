from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.template.loader import render_to_string
from django.template import RequestContext

def loginForm(request):    
    csrf_token_value = request.COOKIES['csrftoken']
    return {
        'login' : render_to_string('userforms.html',\
                                   { 'data' : AuthenticationForm().as_table(), 'dst' : 'login', 'csrf_token_value' : csrf_token_value })
    }
    
def signupForm(request):
    csrf_token_value = request.COOKIES['csrftoken']
    return {
        'signup' : render_to_string('userforms.html',\
                                    { 'data' : UserCreationForm().as_table(), 'dst' : 'signup', 'csrf_token_value' : csrf_token_value })
    }
    
def logoutForm(request):
    csrf_token_value = request.COOKIES['csrftoken']
    return {
        'logout' : render_to_string('userforms.html',\
                                    { 'data' : '<tr><td><input type="submit" value="Logout" /></td></tr>',\
                                      'dst' : 'logout',\
                                      'csrf_token_value' : csrf_token_value })
    }
    

import sys, os, consts, re
from menu import Menu, MenuItem
from utilities import decodeRelationalVariable, tabify, writeFile, addURL, handlePercentToken, decodePageKey


def generateHeader(properties):
    """Takes the standard file and adds a header to it"""
    print "Header generated"
    try:
        return "<a href=\"/\"><h1>%s</h1></a>\n" % (properties["website"]["prettyName"])
    except KeyError:
        return ""

def generateMenu(properties):
    """Generates the menu for a given page"""
    #Checks for menu presence
    print "Menu Generated"
    try:
        properties["menu"]
    except KeyError:
        print "No menu"
        return ""

    menu = Menu()
    for item in properties["menu"]:
        menu.addItem(MenuItem(properties["menu"][item]))
        
    menu.sortItems()
    return menu.show()

def generateFooter(properties):
    """Generate footer"""
    print "Footer genreated"
    try:
        owner = properties["website"]["author"]
    except KeyError:
        owner = properties["website"]["name"]

    from datetime import date
    return "<span style='float:right;'>&copy; %d %s</span><span style='float:left;'>Powered by Kaleidoscope</span>" % (date.today().year, owner)

def generatePage(app, name, appPath, parent, properties, top):
    """
    Generate a page given a dict of properties
    
    A page consists of both a view and a template both are generated by this function.
    """

    print "Generating page: " + name

    #basics for each page template
    tabs = 0
    page = "<!-- Generated code for page: " + name + " -->\n" 
    page += tabify("{%% extends \"%s.html\" %%}" % parent, tabs)

    
    #Generate unique portion for each page
    try:
        page += tabify(("{%% block title %%}%s{%% endblock %%}" % properties["title"]), tabs)
    except KeyError:
        pass #no title for page


    #if this is a top level page fill in the content block
    if top:
        try:
            page += "{% block content %}" + handlePercentToken(properties["template"],'{{ ','|safe }}') + "{% endblock %}"
        except KeyError:
            print "Page " + name + " has no content"
    else:#otherwise we just pop everything in assuming the percent tokens are set up right
        try:
            page += handlePercentToken(properties["template"],'{{ ','|safe }}')
        except KeyError:
            print "page " + name + " has no content"

    with open(os.path.join(appPath, 'templates', name+'.html'), 'w') as f:
        f.write(page)
        
    tabs = 0
    #write view
    #urls need to count capture groups
    args = "request"

    try:
        counter = 1
        for symbol in properties["url"]:
            if symbol == "(": #assume matching for now
                args += ",u_" + str(counter)
                counter += 1
    except KeyError:
        pass #didnt have a url
    
    view = ""
    
    #now the definition of the view function
    view += tabify("def %s(%s):" % (name, args), tabs)
    tabs += 1

    #time to call the security function
    try:
        login = properties['security']['login'] #requires a login
    except KeyError:
        login = "False"

    try:
        groups = properties['security']['groups'] #get groups required
    except KeyError:
        groups = ""

    try:
        redirect = "return %s(request)" % properties['security']['fail']
    except KeyError:
        redirect = "return HttpResponse('Denied', status_code=403)"

    view += tabify("if not permissionsCheck(request,%s,'%s'):" % (login,groups), tabs)
    tabs += 1
    view += tabify(redirect, tabs)
    tabs -= 1

    #time to define variables in the page
    view += tabify("d = {}",tabs) #to hold the variables
    for key in iter(properties):
        if key not in ["title", "url", "template", "pages", "security"]: #predefined keys, anything else is a variable
            view += decodePageKey(key,properties[key],tabs)

    view += tabify("return render(request,\"%s.html\",d)" % name, tabs)
    
    #write the view files
    writeFile(os.path.join(appPath, 'views.py'), view, 'a')

    
    #adds a url mapping
    try:
        addURL(properties['url'],"%s.views.%s" % (app, name), name)
    except KeyError:
        pass #wasnt a leaf page, dont really care if its missing a url

    #generate all sub pages
    try:
        for key in iter(properties['pages']):
            generatePage(app, key, appPath, name, properties['pages'][key], False)
    except KeyError:
        pass #this was a leaf page

    
def createPages(properties):
    """Iterate through and create pages"""
    #location of main app is used a lot
    consts.MAIN = os.path.join(consts.PROJECT, 'main')

    #read standard.html file
    with open(os.path.join(consts.MAIN,'templates', 'standard.html'), 'r') as f:
        standard = f.read()

    #now splice in all the content for standard
    #add in the header

    standard = re.sub("{% block header %}", "{%% block header %%}%s"%generateHeader(properties),standard,flags=re.DOTALL)

    #menu
    standard = re.sub("{% block menu %}", "{%% block menu %%}%s"%generateMenu(properties),standard,flags=re.DOTALL)

    #footer
    standard = re.sub("{% block footer %}", "{%% block footer %%}%s"%generateFooter(properties),standard,flags=re.DOTALL)

    #write the new standard.html
    with open(os.path.join(consts.MAIN, 'templates', 'standard.html'), 'w') as f:
        f.write(standard)    

#at the top of a view file
    viewHeader = """from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template.loader import render_to_string
from middletier import permissionsCheck

"""
    writeFile(os.path.join(consts.MAIN, 'views.py'), viewHeader)

    for page in iter(properties["pages"]):
        generatePage("main", page, consts.MAIN, 'standard', properties["pages"][page], True)
#    except KeyError:
  #      print "No web pages to write"

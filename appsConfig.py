from subprocess import call
import sys, os, consts, re
from utilities import tokenizer,writeFile,addURL,handlePercentToken

##################################
## FORM GENERATION
##################################

def generateForm(path,app,model,properties):
    """Generates a single form's code and returns it"""
    formFields = []
    for prop in iter(properties['fields']):
        try:
            if properties['fields'][prop]['form'] == 'True':
                formFields.append(prop)
        except KeyError:
            formFields.append(prop)

    form = "from models import %s\n" % model

    form += "class %sForm(ModelForm):\n" % model
    form += "    class Meta:\n"
    form += "        model = %s\n" % model
    form += "        fields = %s\n\n".replace("[","(").replace("]",")") % formFields
    #add custom labels
    form += "        labels = {\n"
    for field in formFields:
        try:
            form += "            '%s' : _('%s'),\n" % (field, properties['fields'][field]['label'])
        except KeyError:
            pass #no special label was defined so use the default which is what django does automatically
    form += "        }\n"
    
    return form

def generateForms(path,app,properties):
    """Generates a form for each model for easy search/creation"""
    forms = "from django.utils.translation import gettext as _\n"
    forms += "from django.forms import ModelForm\n\n"

    for model in iter(properties):
        forms += generateForm(path,app,model,properties[model])
    
    #write to the forms file
    writeFile(os.path.join(path,'forms.py'), forms)


##################################
## MODEL GENERATION
##################################

def generateModelField(key, properties):
    """Takes a single field's properties and maps it to a a django object
    the key is the variable name"""

    field = ""
    first = True
    try:
        #test for special cases

        #case 1 ForeignKey
        if properties['type'] == 'ForeignKey':
            target = properties['link']
            if '->' in target:
                imports = target.split('->')
                target = imports[1]
                field += "    from %s.models import %s\n" % (imports[0],imports[1])
            field += "    %s = models.ForeignKey(%s" % (key, target)
            first = False
        elif properties['type'] == 'CharField':
            field += "    %s = models.CharField(max_length=%d" % (key, properties['length'])
        else:
            field += "    %s = models.%s(" % (key, properties["type"])
    except KeyError:
        return  ""

    try:
        required = "blank=True,null=True"
        argstring = properties["argstring"]
        if first:
            first = False
        else:
            argstring += ","+required

        field += "%s)" % argstring

    except KeyError:
        field += ")"

    
    return field + "\n"

def generateModel(path,app,model,properties):
    """generates a specific model"""
    name = model
    print "Generating Model: " + name
    modelStr = "class %s(models.Model):\n" % name

    #process fields
    try:
        for key in iter(properties["fields"]):
            modelStr += generateModelField(key,properties["fields"][key])
    except KeyError:
        modelStr += "    pass"

 
    #register it in the admin panel right before returning it       
    writeFile(os.path.join(path,'admin.py'),\
              "\nfrom django.contrib import admin\nfrom models import %s\nadmin.site.register(%s)\n" % (name,name),\
              mode='a')

    #write the unicode function for admin display if nessisary
    try:
        remapped = tokenizer(properties["admin"],'self.')
        modelStr += "\n    def __unicode__(self):\n    "
        modelStr += "    return " + remapped + "\n"

    except KeyError:
        pass #no special instructions for rendering
    
    return modelStr + "\n"
    
def generateModels(path,app,properties):
    """Generates models for a given app"""

    print "Generating models for app: " + app
    models = "from django.contrib.auth.models import User\nfrom django.db import models\n\n"

    for model in iter(properties):
        models += generateModel(path, app, model, properties[model])
        
    #write the model
    writeFile(os.path.join(path,'models.py'), models)


def writeModelTemplate(path,app,model,properties):
    """Generates the template file for the specified model"""
    t = "<div>"
    try:
        t += handlePercentToken(properties['display'], '{{ obj.', ' }}')
    except KeyError:    #single object template if there exists no display property
        for field in iter(properties["fields"]):
            t += "\n{{ obj.%s }}" % (field)

    t += "\n</div>"
    print "writing", os.path.join(path,'templates',app+'_'+model+'.html')
    with open(os.path.join(path,'templates',app+'_'+model+'.html'), 'w') as f:
        f.write(t)


    #multiple object template
    t = "<div>\n<ul>\n"
    t += "{% for o in objs %}\n"
    try:
        t += "    <li>%s</li>\n" % handlePercentToken(properties['listing'], "{{ o.", " }}")
    except KeyError:
        t += "    <li>{{ o.pk }}</li>\n"
    t += "{% endfor %}\n</ul>\n</div>\n"
    with open(os.path.join(path,'templates',app+'_'+model+"List.html"), 'w') as f:
        f.write(t)
    
######################
## WRITE MODEL VIEWS
######################


def writeModelView(path,app,model,properties):
    """Write a view for the template generated by the above function"""

    view = "\ndef get%s(args):\n" % model
    view += "    if len(args) == 1:\n"
    view += "        return render_to_string('%s_%s.html',{ 'obj' : args[0] })\n" % (app, model)
    view += "    else:\n"
    view += "        return render_to_string('%s_%sList.html',{ 'objs' : args })\n" % (app, model)

    with open(os.path.join(path,'views.py'), 'a') as f:
        f.write(view)
    
def generateModelView(path,app,properties):
    """Generate template and view for this model"""
    print "Generate templates and views"

    #going to need render_to_string in most views so import it everywhere
    with open(os.path.join(path,'views.py'), 'a') as f:
        f.write('from django.template.loader import render_to_string\n')



    #generate the single item view/template and multi item template
    for model in iter(properties):
        writeModelTemplate(path,app,model,properties[model])
        writeModelView(path,app,model,properties[model])


def generateMiddletierForModel(app, model, properties):
    """Generate portion of middletier file for a particular model"""
    result = "\n\n#interactions for model " + model + "\n"

    fields = properties['fields']
    unique = []
    required = []
    for field in iter(fields):
        if 'unique' in fields[field].keys():
            unique.append(field)
        if 'required' in fields[field].keys():
            required.append(field)


    #TODO verify that unique and required are being honored
    #TODO also this is a pretty horrible way to generate these functions, should implemenmt a template system (again) for it

    result += "from django.http import HttpResponse\n"

    #create function
    result += "def create%s(request):\n" % model
    result += "    if request.method == 'POST':\n"
    result += "        data = request.POST.copy()\n"
    result += "        del data['csrfmiddlewaretoken'] #remove this since it is not a part of the object\n"
    result += "        from %s.forms import %sForm\n" % (app,model)
    result += "        form = %sForm(data)\n" % model
    result += "        if form.is_valid():\n"
    result += "            data = form.cleaned_data\n"
    result += "            newObject = %s(**data)\n" % model
    result += "            newObject.save()\n"
    result += "            return HttpResponse('\\'Succesfully Created\\'')\n"
    result += "        return HttpResponse('\\'Data Unclean\\'')\n\n"
    addURL('api/%s/%s/create/'%(app,model),'%s.middletier.create%s'%(app,model),'create_%s' % (model))

    #retrieve function
    result += "def retrieve%s(request):\n" % model
    result += "    if request.method == 'POST':\n"
    result += "        data = request.POST\n"
    result += "        filters = data['filters']\n"
    result += "        qs = %s.objects.filter(**filters)\n" % model
    result += "        return HttpResponse(serializers.serialize([qs]))\n"
    result += "    return HttpResponse('Please send data as POST')\n\n"

    #delete function
    result += "def delete%s(request):\n" % model
    result += "    if request.method == 'POST':\n"
    result += "        data = request.POST\n"
    result += "        filters = data['filters']\n"
    result += "        qs = %s.objects.filter(**filters)\n" % model
    result += "        count = 0\n"
    result += "        for obj in qs:\n"
    result += "            obj.delete()\n"
    result += "            count += 1\n"
    result += "        return HttpResponse('Deleted %s objects' % count)\n"
    result += "    return HttpResponse('Please send data as POST')\n\n"

    #unsure how edit differs from creation/deletion must pontificate

    return result

def generateMiddletier(path,app,properties):
    """Generates the middletier interface to a model"""
    
    mid = "from models import *\nfrom django.core import serializers\n"

    for model in iter(properties):
        mid += generateMiddletierForModel(app, model,properties[model])

    with open(os.path.join(path,'middletier.py'), 'w') as f:
        f.write(mid)

def configureApp(path, app, properties):
    """After it has been created it is populated"""
    print "Configuring app: " + app


    #where to put template chains
    templates = os.path.join(path, 'templates')

    #generate themes
    theme = path + "/static/"
    print "Generating: " + theme
    try:
        call(["mkdir", theme])
        call(["mkdir", templates])
        if call(["cp","-a", os.path.join(consts.RESOURCES, 'themes', properties['theme'],'static','.'), theme]) == 1:
            if call(["cp", "-a", os.path.join(consts.PATH, properties['theme'], 'static',  '.'), theme]) == 1:
                print "Failed to find theme: " + properties['theme'] + " static files"
                sys.exit(1)
        if call(["cp", "-a", os.path.join(consts.RESOURCES, 'themes', properties['theme'], 'templates', '.'), templates]) == 1:
            if call(["cp", "-a", os.path.join(consts.PATH, properties['theme'], 'templates',  '.'), templates]) == 1:
                print "Failed to find theme " + properties['theme'] + " templates"

        call(["cp", "-a", os.path.join(consts.RESOURCES, 'themes', 'core', '.'), theme])
        call(["cp", "-a", os.path.join(consts.RESOURCES, 'templatechains', 'core','.'), templates])
    except:
        print "Failed to generate theme"
    
    #generate the models
    try:
        generateModels(path,app,properties['models'])

        #when done writing models for this app migrate it
        #call([consts.PYTHON, consts.MANAGE, "schemamigration", app, "--intial"])

        #generate default html for displaying the models, these are not fullon pages rather
        #they are small snipets that can be loaded by other pages by using a view to access them
        generateModelView(path,app,properties['models'])
        
        #generate middletier functions for each model
        generateMiddletier(path,app,properties['models'])
        
        #generate the form generators
        generateForms(path,app,properties['models'])
        
    except KeyError:
        #but we still want to make a models file
        writeFile(os.path.join(path,'models.py'), "from django.contrib.auth.models import User")
        print app + " has no models"

    if app == 'main':
        #set urls to callback to the middletier
        addURL('/api/login/', 'main.middletier.login', 'login')
        addURL('/api/logout/', 'main.middletier.logout', 'logout')
        addURL('/api/signup/', 'main.middletier.signup', 'signup')

        #need to put in the context processor that allows us to access login/logout/signout stuff
        call(["cp", os.path.join(consts.RESOURCES,'processors','context_processors.py'),os.path.join(consts.PROJECT,'main','context_processors.py')])
        #copy in the middletier
        call(["cp", os.path.join(consts.RESOURCES,'middletier','middletier.py'),os.path.join(consts.PROJECT,'main','middletier.py')])
        #copy in the form data
        call(["cp", os.path.join(consts.RESOURCES,'userforms.html'),os.path.join(consts.PROJECT,'main','templates','userforms.html')])
        

        
def createApps(properties, theme):
    """Generates all the apps required by the project"""

    name = properties["website"]["name"]
    consts.PYTHON = os.path.join(consts.ENV, 'bin', 'python')
    consts.PROJECT = os.path.join(consts.ENV, name)
    consts.MANAGE = os.path.join(consts.PROJECT, "manage.py")


    #create main app
    try:
        properties["apps"]
    except KeyError:
        properties["apps"] = {}

    properties["apps"]["main"] = { "templatechain" : theme, 
                                   "theme" : theme }

    #create apps and configure them after creation
    try:
        for app in iter(properties["apps"]):
            if not consts.UPDATE:
                call([consts.PYTHON, consts.MANAGE, "startapp", app])
                call(["mv", os.path.join(consts.ENV, app), consts.PROJECT])
            configureApp(os.path.join(consts.PROJECT, app), app, properties["apps"][app])

    except KeyError:
        print "No apps detected"

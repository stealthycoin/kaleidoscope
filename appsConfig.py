from subprocess import call
import sys, os, consts

def generateModelField(key, properties):
    """Takes a single field's properties and maps it to a a django object
    the key is the variable name"""

    field = ""
    try:
        field += "    %s = models.%s(" % (key, properties["type"])
    except KeyError:
        return  ""

    try:
        required = "blank=True,null=True"
        argstring = properties["argstring"]
        if len(argstring) > 0:
            argstring += ","+required
        else:
            argstring = required
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
    with open(path+"/admin.py", "a") as f:
        f.write("\nfrom models import %s\nadmin.site.register(%s)\n" % (name,name))

    #write the unicode function for display if nessisary
    try:
        tokens = properties["display"] + ' '
        state = 0 #0 normal 1 keyword
        buf = ''
        newString = ""
        variables = []
        for symbol in tokens:
            if state == 0:
                if symbol == '%':
                    state = 1
                else:
                    newString += symbol
            else:
                if symbol == '%':
                    newString += '%'
                    state = 0
                else:
                    if symbol == ' ':
                        newString += symbol
                        state = 0
                        variables.append(buf)
                        buf = ''
                        newString += '%s'
                    else:
                        buf += symbol

        mapping = ""
        first = True
        for var in variables:
            if first:
                first = False
            else:
                mapping += ','
            mapping += 'self.'+var
        modelStr += "\n    def __unicode__(self):\n        return u'%s' %% (%s)" % (newString, mapping)


    except KeyError:
        pass #no special instructions for rendering
    
    return modelStr + "\n"
    
def generateModels(path,app,properties):
    """Generates models for a given app"""

    print "Generating models for app: " + app
    models = "from django.db import models\n\n"

    for model in iter(properties):
        models += generateModel(path, app, model, properties[model])
        
    #write the model
    with open(path+"/models.py", "w") as f:
        f.write(models)
        
def configureApp(path, app, properties):
    """After it has been created it is populated"""
    print "Configuring app: " + app

    #template chain to copy
    templates = os.path.join(path, 'templates')
    print "Generating: " + templates
    try:
        call(["mkdir", templates])
        call(["cp", "-a", "../../resources/templatechains/"+properties["templatechain"]+"/.", templates])
    except:
        print "Failed to generate templates"

    #generate themes
    theme = path + "/static/"
    print "Generating: " + theme
    try:
        call(["mkdir",theme])
        call(["cp","-a","../../resources/themes/"+properties["theme"]+"/.", theme])
    except:
        print "Failed to generate theme"
    
    #generate the models
    try:
        generateModels(path,app,properties["models"])

        #when done writing models for this app migrate it
        call([consts.PYTHON, consts.MANAGE, "schemamigration", app, "--intiial"])

    except KeyError:
        print app + " has no models"
        
def createApps(properties):
    """Generates all the apps required by the project"""

    name = properties["website"]["name"]    
    consts.PYTHON = os.path.join(consts.ENV, 'bin', 'python')
    consts.PROJECT = os.path.join(consts.PATH, name)
    consts.MANAGE = os.path.join(consts.PROJECT, "manage.py")


    #create main app
    try:
        properties["apps"]
    except KeyError:
        properties["apps"] = {}

    properties["apps"]["main"] = { "templatechain" : "default", 
                                   "theme" : "default" }

    #create apps and configure them after creation
    try:
        for app in iter(properties["apps"]):
            call([consts.PYTHON, consts.MANAGE, "startapp", app])
            call(["mv", os.path.join(consts.PATH, app), consts.PROJECT])
            configureApp(os.path.join(consts.PROJECT, app), app, properties["apps"][app])

    except KeyError:
        print "No apps detected"
        

    

from subprocess import call
import sys, os

def generateModelField(key, properties):
    """Takes a single field's properties and maps it to a a django object
    the key is the variable name"""

    field = ""
    try:
        field += "    %s = models.%s(" % (key, properties["type"])
    except KeyError:
        return  ""

    try:
        field += "%s)" % properties["argstring"]
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
    print "Configuring app: " + path

    #template chain to copy
    templates = path + "/templates"
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
        manPath = os.path.dirname(path)
        basePath = os.path.dirname(manPath)
        call([basePath+"/venv/bin/python", manPath+"/manage.py", "schemamigration", app, "--intiial"])

    except KeyError:
        print app + " has no models"
        
def createApps(path, properties):
    """Generates all the apps required by the project"""
    
    tool = path+"/venv/bin/python"
    name = properties["website"]["name"]

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
#            try:
            call([tool, path+"/"+properties["website"]["name"]+ "/manage.py", "startapp", app])
            call(["mv", path+"/"+app, path+"/"+name])
            configureApp(path+"/"+name+"/"+app, app, properties["apps"][app])
 #           except:
          #      print "Error creating apps"
  #              sys.exit(6)
    except KeyError:
        print "No apps detected"
        

    

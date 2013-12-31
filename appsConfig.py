from subprocess import call
import sys

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
    print "Generating Model: " + properties["name"]

    model = "class %s(models.Model):\n" % properties["name"]

    #process fields
    try:
        for key in iter(properties["fields"]):
            model += generateModelField(key,properties["fields"][key])
    except KeyError:
        model += "    pass"

    return model + "\n"
    
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
        

    

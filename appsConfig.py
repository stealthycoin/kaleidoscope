from subprocess import call
import sys

def configureApp(path, app, properties):
    """After it has been created it is populated"""
    print "Configuring app: " + path
    
    #template chain to copy
    templates = path + "/templates"
    print "Generating: " + templates
    try:
        call(["mkdir", templates])
        call(["cp", "-a", "../../resources/templatechains/"+properties["apps"][app]["templatechain"]+"/.", templates])
    except:
        print "Failed to generate templates"

    #generate themes
    theme = path + "/static/"
    print "Generating: " + theme
    try:
        call(["mkdir",theme])
        call(["cp","-a","../../resources/themes/"+properties["apps"][app]["theme"]+"/.", theme])
    except:
        print "Failed to generate theme"
    
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
            try:
                call([tool, path+"/"+properties["website"]["name"]+ "/manage.py", "startapp", app])
                call(["mv", path+"/"+app, path+"/"+name])
                configureApp(path+"/"+name+"/"+app, app, properties)
            except:
                print "Error creating apps"
                sys.exit(6)
    except KeyError:
            print "No apps detected"
        

    
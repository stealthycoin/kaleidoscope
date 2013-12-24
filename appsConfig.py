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
        call(["cp", "-r", "../../resources/templatechains/"+properties["apps"][app]["templatechain"], templates])
    except:
        print "Failed to generate templates"
    
        
        
    
    

def createApps(path, properties):
    """Generates all the apps required by the project"""
    
    tool = path+"/venv/bin/python"
    name = properties["website"]["name"]

    #create main app
    try:
        properties["apps"]
    except KeyError:
        properties["apps"] = {}

    properties["apps"]["main"] = { "templatechain" : "default" }

    #create apps 
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
        

    

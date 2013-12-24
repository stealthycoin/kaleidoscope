import os
import sys
import getopt
import json
from subprocess import call
import settingsConfig, appsConfig


path = os.getcwd()
sys.path.append(path) #this is so we can include the compiled ks dictionary

def setup(properties):
    """
    Creates basic django project

    TODO: Error handling and resuming after failure
    """

    try:
        if not os.path.exists(path+"/venv"):
            call(["virtualenv", path+"/venv"])
    except:
        print "Error creating virtual environment. Make sure it is installed."
        sys.exit(1)
            
    try:
        call(["cp", "../../resources/req.pip", "./"])
        call([path+"/venv/bin/pip", "install", "-r", path+"/req.pip"])
    except:
        print "Error installing django or south"
        sys.exit(2)

    try:
        print "Building project"
        call([path+"/venv/bin/django-admin.py", "startproject", properties["website"]["name"]])
    except:
        print "Error creating django project"
        sys.exit(3)

    try:
        call(["git", "init", path])
    except:
        print "Failed to initialize git"
        sys.exit(4)
    
def readJSONFiles(files):
    """
    Parse whatever format we decide to go with here and return whatever we need to store it
    """
    files = [path+"/"+f for f in files]
    
    dictionary = {}

    for f in files:
        with open(f) as r:
            raw = "".join(r.readlines())
            raw = raw.replace("\n", "")
            d = json.loads(raw)
            for k in d.keys():
                dictionary[k] = d[k]

    return dictionary


def parse(filename):
    properties = {}
    try:
        os.system("../../parser < " + filename)
        from dictionary import d
        properties = d
    except:
        exc_type,exc_value,exc_traceback = sys.exc_info()
        print(exc_type)
        print(exc_value)
        print(exc_traceback)
        sys.exit(1)
    return properties


def copyTemplate(name, properties):
    """Copy the templates into the apps"""
    pass

def main():
    opts, args = getopt.getopt(sys.argv[1:], "spf:t:")
    
    filename = "infile"
    templatechain = "default"
    flags = [o for o,a in opts]

    for o, a in opts:
        if o in ("-f",):
            filename = a
        if o in ("-t",):
            templatechain = a

            
    properties = {}

    #read the json files
    if "-p" in flags:
        properties = parse(path + "/" + filename)

    #create base project
    if "-s" in flags:
        setup(properties)

    
    #configure apps
    appsConfig.createApps(path,properties)    

    #copy in the template chain (this has to happen after app creation because the templates go in main)
    copyTemplate(templatechain, properties)

    #add urls for all pages
    addURLs(properties)

    #after the project is built time to start changing properties in the settings
    settingsConfig.handleSettings(path+"/"+properties["website"]["name"]+"/"+properties["website"]["name"]+"/settings.py", properties)


if __name__ == "__main__":
    main()

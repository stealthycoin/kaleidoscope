import os
import sys
import getopt
import json
from subprocess import call
import settingsConfig, appsConfig, pagesConfig


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

def addURLs():
    """Genreate urls page"""

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

    #configure the pages
    pagesConfig.createPages(path,properties)

    #after the project is built time to start changing properties in the settings
    settingsConfig.handleSettings(path+"/"+properties["website"]["name"]+"/"+properties["website"]["name"]+"/settings.py", properties)

    #intiialize the test database
    print "python " + path+"/"+properties["website"]["name"]+"/manage.py syncdb"
    try:
        call([path+"/venv/bin/python", path+"/"+properties["website"]["name"]+"/manage.py", "syncdb"])
        call([path+"/venv/bin/python", path+"/"+properties["website"]["name"]+"/manage.py", "migrate"])
    except:
        print "failed to initialize the database"

if __name__ == "__main__":
    main()

#!/usr/bin/python
import os, sys, getopt
from subprocess import call
import settingsConfig, appsConfig, pagesConfig
import consts

consts.PATH = os.getcwd()
consts.KSCOPE = os.path.abspath(os.path.dirname(__file__))
consts.RESOURCES = os.path.join(consts.KSCOPE, 'resources')

sys.path.append(consts.PATH) #this is so we can include the compiled ks dictionary

def setup(properties):
    """
    Creates basic django project

    TODO: Error handling and resuming after failure
    """

    try:
        try:
            env = properties["environment"]
        except KeyError:
            env = "venv"
        consts.ENV = os.path.join(consts.PATH, env)

        if not os.path.exists(consts.ENV):
            call(["virtualenv", consts.ENV])
    except:
        print "Error creating virtual environment. Make sure viurtualenv is installed."
        sys.exit(1)
            
    try:
        call(["cp", "../../resources/req.pip", "./"])
        call([os.path.join(consts.ENV, 'bin', 'pip'), "install", "-r", os.path.join(consts.PATH, 'req.pip')])
    except:
        print "Error installing django or south"
        sys.exit(2)

    try:
        print "Building project"
        os.chdir(consts.ENV)
        call([os.path.join(consts.ENV, 'bin', 'django-admin.py'), "startproject", properties["website"]["name"]])
    except OSError as e:
        print "Error creating django project", e
        sys.exit(3)

    try:
             call(["git", "init", consts.PATH])
    except:
        print "Failed to initialize git"
        sys.exit(4)
    
def parse(filename):
    properties = {}
    try:
        os.system("../../parser < %s" % (filename))
        from dictionary import d
        properties = d
    except:
        exc_type,exc_value,exc_traceback = sys.exc_info()
        print(exc_type)
        print(exc_value)
        print(exc_traceback)
        sys.exit(1)
    return properties

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
        properties = parse(os.path.join(consts.PATH, filename))

    #create base project
    if "-s" in flags:
        setup(properties)

    #configure apps
    appsConfig.createApps(properties)    

    #configure the pages
    pagesConfig.createPages(properties)

    #after the project is built time to start changing properties in the settings
    settingsConfig.handleSettings(os.path.join(consts.PROJECT,\
                                               properties["website"]["name"],\
                                               'settings.py'),\
                                  properties)

    #intiialize the test database
    try:
        call([consts.PYTHON, consts.MANAGE, "syncdb"])
    except:
        print "failed to initialize the database"

#entry point
if __name__ == "__main__":
    main()

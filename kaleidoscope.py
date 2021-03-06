#!/usr/bin/python
import os, sys, getopt
from subprocess import call
from utilities import tabify,writeFile
import settingsConfig, appsConfig, pagesConfig, devConfig
import consts, globs

globs.DELETED = []
globs.URLS = []

consts.PATH = os.getcwd()
consts.KSCOPE = os.path.abspath(os.path.dirname(__file__))
consts.RESOURCES = os.path.join(consts.KSCOPE, 'resources')


sys.path.append(consts.PATH) #this is so we can include the compiled ks dictionary

def writeURLS(properties):
    """Writes the urls file, last thing done in the setup process to make sure there are no stray urls to be added"""
    urlfile = """from django.conf.urls import include, patterns, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
"""

    for url in globs.URLS:
        urlfile += tabify(url+",",1)

    urlfile += ")\n"
        
    writeFile(os.path.join(consts.PROJECT,properties['website']['name'],'urls.py'),urlfile)

def handleMakefile(properties):
    """Makefile generation for easy launching of the test site"""
    with open(os.path.join(consts.RESOURCES, 'makefile'), 'r') as f:
        makefile = f.read()

    with open(os.path.join(consts.PATH, 'makefile'), 'w') as f:
        f.write(makefile % (properties['website']['name'],\
                            os.path.join(consts.ENV,'bin','activate'),\
                            os.path.join(consts.ENV,properties['website']['name']),\
                            consts.ENV))

def setup(properties):
    """
    Creates basic django project

    TODO: Error handling and resuming after failure
    """

    try:
        if not os.path.exists(consts.ENV):
            call(["virtualenv", consts.ENV])
    except:
        print "Error creating virtual environment. Make sure viurtualenv is installed."
        sys.exit(1)
            
    try:
        call(["cp", os.path.join(consts.RESOURCES, 'req.pip'), "./"])
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
        os.system("/usr/local/lib/kaleidoscope/parser < %s" % (filename))
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
    opts, args = getopt.getopt(sys.argv[1:], "ut:s:")
        
    filename = "infile"
    flags = [o for o,a in opts]
    arguments = {key: value for (key, value) in opts}



    properties = parse(os.path.join(consts.PATH, args[0]))

    try:
        theme = properties['website']['theme']
    except KeyError:
        theme = "default"

    #setup v environment vars
    try:
        globs.ENVNAME = properties["environment"]
    except KeyError:
        globs.ENVNAME = "venv"
    consts.ENV = os.path.join(consts.PATH, globs.ENVNAME)

    #get the hostname (localhost if none provided)
    try:
        consts.HOSTNAME = properties["website"]["host"]
    except KeyError:
        consts.HOSTNAME = "localhost"

    #try and get the root directory on the server (/webapps otherwise)
    try:
        consts.WEBAPPS = properties["website"]["root"]
    except KeyError:
        consts.WEBAPPS = '/webapps'

    #marked as update update
    if "-u" in flags:
        consts.UPDATE = True #need to modify this to build missing portions
    else:
        setup(properties) #this fn is where the project is built
        consts.UPDATE = False

    #configure apps
    appsConfig.createApps(properties, theme)    

    #configure the pages
    pagesConfig.createPages(properties)

    #write the urls page
    writeURLS(properties)

    #after the project is built time to start changing properties in the settings
    settingsConfig.handleSettings(os.path.join(consts.PROJECT,\
                                               properties["website"]["name"],\
                                               'settings.py'),\
                                  properties)

    #prepare the configuration files for the dev environment
    devConfig.createDevFiles(properties)

    #copy the makefile over
    handleMakefile(properties)

    #if there are static files copy them
    if "-s" in flags:
        call(["cp", "-a", os.path.join(consts.PATH, arguments["-s"], "."), os.path.join(consts.MAIN, 'static')])

    #intiialize the test database
    try:
        call([consts.PYTHON, consts.MANAGE, "syncdb"])
    except:
        print "failed to initialize the database"

#entry point
if __name__ == "__main__":
    main()

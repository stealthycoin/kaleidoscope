import re,consts,os,random
from utilities import tupleEntrys
from utilities import showDatabaseDictionary as showDD
from subprocess import call
from utilities import writeFile

def handleMiddleware(settings,properties):
    """Generate the list of middlware classes to be used"""
    
    middle = """MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)"""

    return "%s\n\n#Middleware classes\n%s" % (settings,middle)

def generateSecretKey(settings):
    """Makes and adds a secretkey to the settings file"""
    key = ''.join([random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])
    return "%s\nSECRET_KEY = '%s'" % (settings,key) 
    


def handleStatic(settings,properties):
    """Add static settings"""
    lines = settings.split("\n")
    mark = 2
    for line in lines:
        if "STATIC_URL" in line:
            break
        mark += 1
    
    newLines = ["STATIC_ROOT = os.path.join(BASE_DIR,'static')", "", "STATICFILE_DIRS = ("]
    
    for app in iter(properties["apps"]):
        newLines.append("    os.path.join(BASE_DIR,'%s/static/')," % app)

    newLines += [")"]
    
    result = lines[:mark] + newLines + lines[mark:]

    return "\n".join(result)
    

def handleTemplates(settings,properties):
    """Generates the template names"""

    settings += "\n"

    apps = properties["apps"]
    result = "\n#Template directories\nTEMPLATE_DIRS = (\n"
    apps = map(lambda x: "os.path.join(BASE_DIR, '%s/templates')" % (x), apps)
    apps = tupleEntrys(apps,True) #encode for tuple
    result += "\n".join(apps) + "\n)"
    
    return settings + result

def handleApps(settings,properties):
    """Adds south and whatever other apps necessary"""

    apps = ['south','main','django.contrib.admin','django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions','django.contrib.sites','django.contrib.messages','django.contrib.staticfiles'] #always include south and main
    
    try:
        for app in iter(properties["apps"]):
            apps.append(app)
    except KeyError:
        pass #no apps, we will get an error about this in the appsConfig

    
    apps =  map(lambda x:"    '%s'," % x, apps)
    settings += "\nINSTALLED_APPS = (\n" + '\n'.join(apps) + ")"
    
    return settings

def handleDatabase(settings,properties):
    """Configure the datbase settings"""

    #cut out default database
    lines = settings.split("\n")
    mark = 0
    for line in lines:
        if line.startswith("# Database"):
            break
        mark += 1
        
    lines = lines[:mark] + lines[mark+9:]
    settings = "\n".join(lines)

    try:
        newDict = {}
        for key in iter(properties["database"]):
            newDict[key.upper()] = properties["database"][key]
    except KeyError:
        return settings
    
    return "%s\nDATABASES = { 'default': %s }\n" % (settings, showDD(newDict))
    

def handleAdmins(settings,properties):
    """Configures admins in the settings file"""
    website = properties["website"] #this is ensured by the parser
    
    print "Adding administrators"

    addstring = "\n#Administrators\nADMINS = (\n"
    try:
        admins = website["admins"]
        adminList = []
        
        for key in admins:
            name, email = admins[key]['name'], admins[key]['email']
            print "Found admin: %s" % name
            adminList.append("('%s', '%s')" % (name, email))

        adminList = tupleEntrys(adminList,True)
        addstring += "\n".join(adminList) + "\n"
        
        
    except KeyError:
        print "No administrators specified."

    addstring += ")\n"

    return settings + "\n" + addstring


def handleSettings(settings_file, properties):
    """Reads the settings file and calls functions to edit it using properties
       Once this is done it writes any changes and closes the file"""

    #important basics might be editable later for now constant
    contents = "import os\n"
    contents += "BASE_DIR = os.path.dirname(os.path.abspath(__file__))\n\n"

    contents += "SITE_ID = 1\n"

    contents += "DEBUG = True\nTEMPLATE_DEBUG=DEBUG\n" #different in different sub settings files

    contents += "ALLOWED_HOSTS = ['']\n\n" #this needs to be changable

    contents += "ROOT_URLCONF = '%s.urls'\n" % properties['website']['name']

    contents += "STATIC_URL = '/static/'\n"

    contents += "WSGI_APPLICATION = '%s.wsgi.application'" % properties['website']['name'] #this is only for testing env

    #middleware
    contents = handleMiddleware(contents,properties)

    #generate secret key
    contents = generateSecretKey(contents)

    #add administrators
    contents = handleAdmins(contents,properties)
    contents += "MANAGERS = ADMINS\n"


    #add installed apps and south
    contents = handleApps(contents,properties)

    #add in template dirs at the end
    contents = handleTemplates(contents,properties)

    #add static dirs and root
    contents = handleStatic(contents,properties)

    #setup the database
    contents = handleDatabase(contents,properties)

    #rewite changes
    writeFile(settings_file,contents)

    #last thing is to delete the pyc of the settings file otherwise it will be out of date
    call(["rm", settings_file + "c"])
    

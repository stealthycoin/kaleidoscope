import re
from utilities import tupleEntrys
from utilities import showDatabaseDictionary as showDD
from subprocess import call

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
    lines = settings.split("\n")
    i = 1
    for line in lines:
        if "INSTALLED_APPS" in line:
            break
        i += 1

    apps = ["south"] #always include south and main
    
    try:
        for app in iter(properties["apps"]):
            apps.append(app)
    except KeyError:
        pass #no apps, we will get an error about this in the appsConfig

    
    apps =  map(lambda x:"'%s'" % x, apps)
    result = lines[0:i] + tupleEntrys(apps) + lines[i:] 
    
    return '\n'.join(result)

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

    addstring = ""
    try:
        admins = website["admins"]
        adminList = []
        addstring = "\n#Administartors\nADMINS = (\n"
        
        for key in admins:
            name, email = admins[key]['name'], admins[key]['email']
            print "Found admin: %s" % name
            adminList.append("('%s', '%s')" % (name, email))

        adminList = tupleEntrys(adminList,True)
        addstring += "\n".join(adminList) + "\n)"
        
        
    except KeyError:
        print "No administrators specified."

    return settings + "\n" + addstring


def handleSettings(settings_file, properties):
    """Reads the settings file and calls functions to edit it using properties
       Once this is done it writes any changes and closes the file"""

    f = open(settings_file, "r")
    contents = f.read()
    f.close()
    
    #add administrators
    contents = handleAdmins(contents,properties)

    #add installed apps and south
    contents = handleApps(contents,properties)

    #add in template dirs at the end
    contents = handleTemplates(contents,properties)

    #add static dirs and root
    contents = handleStatic(contents,properties)

    #setup the database
    contents = handleDatabase(contents,properties)

    f.close()

    #rewrite changes
    f = open(settings_file, "w")
    f.write(contents)
    f.close()

    #last thing is to delete the pyc of the settings file otherwise it will be out of date
    call(["rm", settings_file + "c"])
    

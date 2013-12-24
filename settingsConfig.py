import re

def handleApps(settings,properties):
    """Adds south and whatever otehr apps necessary"""
    lines = settings.split("\n")
    i = 1
    for line in lines:
        if "INSTALLED_APPS" in line:
            break
        i += 1

    apps = ["    'south',", "    'main',"] #always include south
    
    try:
        for app in iter(properties["apps"]):
            apps.append("    '"+app+"',")
    except KeyError:
        pass #no apps, we will get an error about this in the appsConfig

    result = lines[0:i] + apps + lines[i:] 
    return '\n'.join(result)

def handleAdmins(settings,properties):
    """Configures admins in the settings file"""
    website = properties["website"] #this is ensured by the parser
    
    print "Adding administrators"

    try:
        admins = website["admins"]
        addstring = "ADMINS = ("
        first = True
        for key in admins:
            name, email = admins[key]['name'], admins[key]['email']
                
            admin = "('%s', '%s'),\n" % (name, email)
            if first:
                first = False
                admin += "\t"

            addstring += admin
            print "Found admin: %s" % admin[0:-2]
        addstring = addstring[0:-2] + ")"
        
    except KeyError:
        print "No administrators specified."

    return settings + "\n" + addstring


def handleSettings(settings_file, properties):
    """Reads the settings file and calls functions to edit it using properties
       Once this is done it writes any changes and closes the file"""

    f = open(settings_file, "r")
    contents = f.read()

    #add administrators
    contents = handleAdmins(contents,properties)

    #add installed apps and south
    contents = handleApps(contents,properties)

    f.close()

    #rewrite changes
    f = open(settings_file, "w")
    f.write(contents)
    f.close()

import re

def handleApps(settings,properties):
    """Adds south and whatever otehr apps nessissary"""

    lines = settings.split("\n") #use this later by splicing an array of new apps into the array of lines at the correct line (one after installed apps = )

    #add south
    settings = settings.replace("INSTALLED_APPS = (", "INSTALLED_APPS = (\n    'south',")
    return settings

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

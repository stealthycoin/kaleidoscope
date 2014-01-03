
def tupleEntrys(l,removeLastComma = False):
    """Takes a list of elements and returns a list of elements prepared to be inserted into a tuple"""

    l = map(lambda x:"    %s," % x, l) #encode into format for tuple (tabbed and comma sep)
    if removeLastComma: #this is needed when our entries make up the whole tuple, rather than being spliced into the middle of an existing list
        l[-1] = l[-1][:-1] #strip off last comma

    return l
        


def showDatabaseDictionary(d):
    """tricky because some elements need to not be quoted like NAME"""

    result = "{\n"
    first = True

    for key in iter(d):
        if first:
            first = False
        else:
            result += ", "
        if key == "NAME":
            result += "'NAME' : os.path.join(BASE_DIR, '%s')" % d[key]
        else:
            result += "'%s' : '%s'" % (key, d[key])
            

    return result + "\n}"

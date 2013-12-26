
def tupleEntrys(l,removeLastComma = False):
    """Takes a list of elements and returns a list of elements prepared to be inserted into a tuple"""

    l = map(lambda x:"    %s," % x, l) #encode into format for tuple (tabbed and comma sep)
    if removeLastComma: #this is needed when our entries make up the whole tuple, rather than being spliced into the middle of an existing list
        l[-1] = l[-1][:-1] #strip off last comma

    return l
        

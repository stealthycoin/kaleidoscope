
def tupleEntrys(l,removeLastComma = False):
    """Takes a list of elements and returns a list of elements prepared to be inserted into a tuple"""

    l = map(lambda x:"    %s," % x, l) #encode into format for tuple (tabbed and comma sep)
    if removeLastComma: #this is needed when our entries make up the whole tuple, rather than being spliced into the middle of an existing list
        l[-1] = l[-1][:-1] #strip off last comma

    return l

def showDatabaseDictionary(d):
    """tricky because some elements need to have things inserted into them like NAME"""

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

def tokenizer(string, accessor="", context=""):
    """Takes in a string and replaces %word with '%s' % (word)"""

    tokens = string
    state = 0 #0 normal 1 keyword
    buf = ''
    newString = ""
    variables = []
    for symbol in tokens:
        if state == 0:
            if symbol == '%':
                state = 1
            else:
                newString += symbol
        else:
            if symbol == '%':
                newString += '%'
                state = 0
            else:
                if symbol == ' ':
                    state = 0
                    variables.append(buf)
                    buf = ''
                    newString += '%s '
                else:
                    buf += symbol
                    mapping = ""
                    first = True
    
    if state == 1:
        state = 0
        variables.append(buf)
        buf = ''
        newString += '%s'

    for var in variables:
        if first:
            first = False
        else:
            mapping += ','
        mapping += accessor+var
    
    return "'%s' %% (%s)" % (newString, mapping)

#test the thingies
def testTok():
    assert tokenizer('%name and then %type','self.%s') == "'%s and then %s' % (self.name,self.type)", "Oh god its wrong! 1"
    assert tokenizer('%name','self.%s') == "'%s' % (self.name)", "Oh god its wrong! 2"


if __name__ == '__main__':
    testTok()

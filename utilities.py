import re,os,consts,globs

C = 0 #global counter to make relations unique

def addURL(url,mapping,name):
    """Takes a url mapping and a name for it and adds it to the global URL list to be added at the end of kscope"""
    urlstring = "url('^%s$','%s',name='%s')" % (url,mapping,name)
    globs.URLS.append(urlstring)


def writeFile(path,content,mode='w'):
    """Takes care of writing a file and automatically uses consts.UPDATE to figure out what files to change"""
    
    filename = os.path.basename(path)
    ksfilename = "ks_" + filename
    pathname = os.path.dirname(path)
    pre = ''

    #if mode is append (a) we need to read the old ks file if possible and append new content to it. If it doesnt exist use w mode
    if mode == 'a':
        try:
            with open(os.path.join(pathname,ksfilename),'r') as f:
                pre = f.read()
        except IOError:
            #no file exists to append to so write like normal
            writeFile(path,content)
            return


    if not consts.UPDATE: #it is not an update so we have to generate all files including the ones that the person might make
        with open(os.path.join(pathname,filename),'w') as f:
            f.write("from %s import *\n\n#write your own content here, this file will not be overwritten when using the -u option in kaleidoscope" % (ksfilename[:-3]))

    with open(os.path.join(pathname,ksfilename),'w') as f: #write the ks generated file
        f.write(pre+"\n"+content)

        

    

def tabify(string, tabs):
    """Adds tabs before string"""
    return ("    " * tabs) + string + "\n"


def decodeRelationalVariable(key,value,tabs):
    """Takes in a relational variable and returns python code to define it"""
    global C
    relation = re.compile('(S|F)\[(.*)\]\((\w+)->(\w+)\)\|(.*)')
    m = relation.search(value)
    
    result = ""
    
    if m.group(1) == 'F': #Form selection
        result = tabify("from %s.models import %s" % (m.group(3),m.group(4)), tabs)
        result += tabify('r%d = {}' % C, tabs)
        

        #restrictions exist so this is an edit form
        if m.group(2) is not '':
            #generate a form for editing the object by going to the url /app/model/edit and sending the form data
            form = "<h2>Edit %s</h2><form action=\"/api/%s/%s/edit/\" method=\"POST\">{%%%% csrf_token %%%%}%s<input type=\"submit\"></form>" % (m.group(4), m.group(3), m.group(4), "%s")

            for restriction in m.group(2).split(','):
                pair = restriction.split('=')
                result += tabify("try:",tabs)
                tabs += 1
                result += tabify("r%d['%s'] = %s" % (C,pair[0], pair[1].replace('%', 'u_')), tabs)
                result += tabify("objToForm = %s.objects.get(**r%d)" % (m.group(4), C) ,tabs)
                result += tabify("from %s.forms import %sForm" % (m.group(3),m.group(4)),tabs)
                result += tabify("form = %sForm(instance=objToForm)" % (m.group(4)), tabs)
                result += tabify("d['%s'] = '%%s' %% ('%s' %% form.as_p())" % (key, form), tabs)
                tabs -= 1
                result += tabify("except %s.DoesNotExist:" % m.group(4), tabs)
                tabs += 1
                result += tabify("d['%s'] = '%s'" % (key,m.group(5)), tabs)
                tabs -= 1
                
        else: #in this case we have a creation form as no query was requested
            result += tabify("from django.template import RequestContext",tabs)
            result += tabify("from %s.forms import %sForm" % (m.group(3),m.group(4)), tabs)
            result += tabify("d['%s'] = render_to_string('form.html',{'title': 'Create %s', 'action' : '/api/%s/%s/create/', 'formFields' : %sForm().as_p()}, context_instance=RequestContext(request))" % (key, m.group(4), m.group(3), m.group(4), m.group(4)), tabs)

    elif m.group(1) == 'S': #Selection
        result = tabify("from %s.views import get%s, get%sList" % (m.group(3),m.group(4),m.group(4)), tabs)
        result += tabify('r%d = {}' % C, tabs)
        if m.group(2) is not '':
            for restriction in m.group(2).split(','):
                pair = restriction.split('=')
                result += tabify("r%d['%s'] = %s" % (C, pair[0], pair[1].replace('%', 'u_')), tabs)

        result += tabify("d['%s'] = get%s(r%s)" % (key, m.group(4), C) ,tabs)

    C += 1
    return result

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

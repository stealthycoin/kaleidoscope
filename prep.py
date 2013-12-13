import os
import sys
import getopt
import json
from subprocess import call

path = os.path.dirname(os.path.realpath(__file__))

def setup(properties):
    """
    Creates basic django project

    TODO: Error handling and resuming after failure
    """

    try:
        if not os.path.exists(path+"/venv"):
            call(["virtualenv", path+"/venv"])
    except:
        print "Error creating virtual environment. Make sure it is installed."
        sys.exit(1)
            
    try:
        call([path+"/venv/bin/pip", "install", "-r", path+"/req.pip"])
    except:
        print "Error installing django or south"
        sys.exit(2)

    try:
        call([path+"/venv/bin/django-admin.py", "startproject", properties["website"]["name"]])
    except:
        print "Error creating django prject"
        sys.exit(3)
        
    
def readJSONFiles(files):
    """
    Parse whatever format we decide to go with here and return whatever we need to store it
    """
    files = [path+"/"+f for f in files]
    
    dictionary = {}

    for f in files:
        with open(f) as r:
            raw = "".join(r.readlines())
            raw = raw.replace("\n", "")
            d = json.loads(raw)
            for k in d.keys():
                dictionary[k] = d[k]

    return dictionary

def main():
    opts, args = getopt.getopt(sys.argv[1:], "spf:")
    
    filename = "infile"
    flags = [o for o,a in opts]

    for o, a in opts:
        if o in ("-f",):
            filename = a

            
    properties = {}

    #read the json files
    if "-p" in flags:
        properties = readJSONFiles(args)

    #create base project
    if "-s" in flags:
        setup(properties)

if __name__ == "__main__":
    main()

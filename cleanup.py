import sys,os,shutil

tests = ["homepage", "epicprof"]

for test in tests:
    path = "./tests/"+test+"/"
    for f in os.listdir(path):
        if os.path.isdir(path+f):
            shutil.rmtree(path+f)
        else:
            if not f.endswith('.ks') and not f.endswith('.html'):
                os.remove(path+f)

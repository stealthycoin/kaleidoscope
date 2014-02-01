import sys,os,shutil
from subprocess import call

tests = ["ai", "epicprof", "penelopy"]
old = os.getcwd()
for test in tests:
    path = "./tests/"+test+"/"
    os.chdir(path)
    call(["make","nuke"])
    os.chdir(old)

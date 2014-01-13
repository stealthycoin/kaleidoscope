import sys,os,errno,shutil

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def main():
    """Install all the things!"""
    PATH = sys.argv[1]

    BIN = os.path.join(PATH, 'bin')
    LIB = os.path.join(PATH, 'lib', 'kaleidoscope')

    mkdir_p(LIB)

    #copy files
    LIB_FILES = ['utilities.py','kaleidoscope.py','consts.py','globs.py','menu.py','appsConfig.py','pagesConfig.py','settingsConfig.py','utilities.py','parser']

    for f in LIB_FILES:
        shutil.copy2(f,LIB)

    #copy resources dir
    shutil.copytree('resources/',os.path.join(LIB,'resources'))

    #write the launch script
    with open(os.path.join(BIN,'kaleidoscope'), 'w') as f:
        f.write("python2.7 %s \"$@\"\n" % os.path.join(LIB, 'kaleidoscope.py'))
              


if __name__ == '__main__':
    main()

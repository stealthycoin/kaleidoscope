import consts, globs
import os,sys

def createNGINXConf(properties):
    consts.NGINX = os.path.join(consts.ENV, 'nginx')
    try:
        os.mkdir(consts.NGINX)
    except:
        pass #already existed I guess.

    with open(os.path.join(consts.RESOURCES,'nginx.conf'), 'r') as f:
        conf = f.read()
        
    name = properties['website']['name']

    with open(os.path.join(consts.NGINX,'%s.nginxconf'%name), 'w') as f:
        f.write(conf % (name,consts.WEBAPPS,name,name,consts.WEBAPPS,name,consts.WEBAPPS,name,consts.WEBAPPS,name,consts.WEBAPPS,name,name,consts.WEBAPPS,name))


def createRunAppScript(properties):
    """Creates the script to launch the web application"""
    with open(os.path.join(consts.RESOURCES,'launch_script'), 'r') as f:
        script = f.read()

    name = properties['website']['name']
    path = os.path.join(consts.WEBAPPS,globs.ENVNAME)
                        
    with open(os.path.join(consts.ENV, 'bin', 'launch_%s'%name), 'w') as f:
        f.write(script % (name,\
                          path,name,\
                          path+"/run/gunicorn.sock",\
                          name,\
                          name,\
                          name))


def createDevFiles(properties):
    """Creates the configuration files for setting up a blank linux server"""
    #generate the config file for nginx
    createNGINXConf(properties)
                        
    #generate the run_app script
    createRunAppScript(properties)
                        

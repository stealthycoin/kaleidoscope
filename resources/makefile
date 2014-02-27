####################################
### Kaleidoscope Powered %s makefile
####################################
SHELL := /bin/bash

#launches the test server address 127.0.0.1:8000
test:
	source %s;\
	python %s/manage.py runserver

#destroys whole project. Probably don't want to use this unless starting over.
nuke:
	rm -rf dictionary.py dictionary.pyc %s req.pip makefile *~

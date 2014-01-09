SHELL := /bin/bash

main: main.cpp parser.cpp tokens.cpp
	g++ -std=c++11 -o parser *.cpp
parser.cpp : grammar.y
	bison -d -o parser.cpp grammar.y
tokens.cpp : scanner.l
	flex -o tokens.cpp scanner.l

.PHONY: clean
clean:
	-python cleanup.py

.PHONY: spotless
spotless: clean
	-rm parser tokens.cpp parser.cpp parser.hpp *~ *.pyc

.PHONY: prof
prof:
	cd tests/epicprof/;\
	python ../../kaleidoscope.py -p -f epicprofessors.ks;\
	source venv/bin/activate;\
	python venv/EpicProfs/manage.py runserver

.PHONY: update
update:
	cd tests/epicprof;\
	python ../../kaleidoscope.py -pu -f epicprofessors.ks;\
	source venv/bin/activate;\
	python venv/EpicProfs/manage.py runserver

.PHONY: test
test:
	cd tests/homepage/ ;\
	python ../../kaleidoscope.py -p -f homepage.ks;\
	source venv/bin/activate;\
	python venv/Homepage_Testing/manage.py runserver

save:
	cp tests/homepage/venv/Homepage_Testing/db.db ~/db.db

restore:
	cp ~/db.db tests/homepage/venv/Homepage_Testing/db.db

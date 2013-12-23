TESTS="basic stupid"

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

.PHONY: test
test:
	cd ./tests/basic/ ;\
	python ../../kaleidoscope.py -ps -f basic.ks ;\

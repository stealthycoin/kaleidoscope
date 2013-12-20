main: main.cpp parser.cpp tokens.cpp
	g++ -std=c++11 -o parser *.cpp
parser.cpp : grammar.y
	bison -d -o parser.cpp grammar.y

tokens.cpp : scanner.l
	flex -o tokens.cpp scanner.l

clean:
	rm parser tokens.cpp parser.cpp

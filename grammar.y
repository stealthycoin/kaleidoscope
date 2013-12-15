%{
#include "node.h"
ObjectNode *root;
%}


%token TOK_RIGHTCURLY TOK_LEFTCURLY TOK_COMMA

%union {
       Node *node;
       std::vector<EntryNode> *entryVec;
       std::string string;
       double number;
}


%token TOK_KEY
%token TOK_STRING
%token TOK_NUMBER
%token TOK_COLON


%type <node> start object entry value;
%type <entryVec> entries
%type <number> TOK_NUMBER TOK_KEY;
%type <string> TOK_STRING;

%start start

%%

start             : object              { root = $1; }
                  ;

object            : '{' entries '}'     { $$ = new ObjectNode($2); }
                  ;

entries           : entry               { $$ = new std::vector<EntryNode>(); $$->push_back($1); }
                  | entry ',' entries   { $$ = $3->push_back($1); }
		  ;

entry             : TOK_KEY ':' value   {$$ = new EntryNode($1, $3); }
                  ; 

value             : object              { $$ = $1; }       
                  | TOK_STRING          { $$ = new StringNode($1); }
                  | TOK_NUMBER          { $$ = new NumberNode($1); }   
                  ; 


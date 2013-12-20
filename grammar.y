%{
#include "node.hpp"
ObjectNode *root;

 extern int yylex();
 void yyerror(const char *s) { printf("ERROR:%s\n", s); }
%}

%token TOK_RIGHTCURLY TOK_LEFTCURLY TOK_COMMA TOK_COLON

%union {
  Node *node;
  ObjectNode *object;
  EntryNode *entry;
  std::vector<EntryNode*> *entryVec;


  double number;
  std::string *str;

  std::string *string;
  int token;
}

%token <number> TOK_NUMBER;
%token <str> TOK_STRING TOK_KEY;

%type <object> start object;
%type <entry> entry; 
%type <node> value;
%type <entryVec> entries

%start start

%%

start             : object              { root = $1; }
                  ;

object            : '{' entries '}'     { $$ = new ObjectNode(*$2); }
                  ;

entries           : { $$ = NULL; } 
                  | entry               { $$ = new std::vector<EntryNode*>(); $$->push_back($1); }
                  | entry ',' entries   { $3->push_back($1); $$ = $3; }
		  ;

entry             : TOK_KEY ':' value   { $$ = new EntryNode(*$1, $3); }
                  ; 

value             : object              { $$ = $1; }       
                  | TOK_STRING          { $$ = new StringNode(*$1); }
                  | TOK_NUMBER          { $$ = new NumberNode($1); }   
                  ; 


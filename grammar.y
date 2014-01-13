%{
#include "node.hpp"
ObjectNode *root;

 extern int yylex();
 extern char*yytext;
 extern int yylineno;

 void yyerror(const char *msg) {
   printf("%d: %s at '%s'\n", yylineno, msg, yytext);
 }

%}

%token TOK_RIGHTCURLY TOK_LEFTCURLY TOK_COMMA TOK_COLON TOK_FILE
%token TOK_RIGHTBRACKET TOK_LEFTBRACKET TOK_S TOK_F TOK_ARROW TOK_EQUAL TOK_LEFTPAREN TOK_RIGHTPAREN

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

start             : entries              { root = new ObjectNode(*$1); }
                  | object               { root = $1; }
                  ;

object            : TOK_LEFTCURLY entries TOK_RIGHTCURLY     { $$ = new ObjectNode(*$2); }
                  | TOK_LEFTCURLY TOK_RIGHTCURLY             { $$ = new ObjectNode(); }
                  ;

entries           : entry                     { $$ = new std::vector<EntryNode*>(); $$->push_back($1); }
                  | entry TOK_COMMA entries   { $3->push_back($1); $$ = $3; }
		  ;

entry             : TOK_KEY TOK_COLON value   { $$ = new EntryNode(*$1, $3); }
                  ; 

value             : object              { $$ = $1; }       
                  | TOK_STRING          { $$ = new StringNode(*$1); }
                  | TOK_NUMBER          { $$ = new NumberNode($1); } 
                  | TOK_FILE TOK_STRING { $$ = new FileNode(*$2); }  
                  | relation_expr       { std::string *s = new std::string("expression"); $$ = new StringNode(*s); }
                  ; 


/* Relation expression rules */

relation_expr     : relation_rule restrictions operation_set { }
                  ;

/* RESTRICTIONS */
restrictions      : TOK_LEFTBRACKET restriction_list TOK_RIGHTBRACKET { } 
                  | TOK_LEFTBRACKET TOK_RIGHTBRACKET                  { } 
                  ;

restriction_list  : restriction                            {  }
                  | restriction_list TOK_COMMA restriction {  }
                  ;

restriction       : TOK_KEY TOK_EQUAL restriction_val
                  ;

restriction_val   : TOK_STRING          { }
                  | TOK_NUMBER          { }
                  | TOK_FILE TOK_STRING { }
                  ;

relation_rule     : TOK_S             {  }
                  | TOK_F             {  }
                  ;

/* OPERATION SETS */

operation_set     : TOK_LEFTPAREN set TOK_RIGHTPAREN  { }
                  ;

set               : TOK_KEY TOK_ARROW TOK_KEY { }
                  ;

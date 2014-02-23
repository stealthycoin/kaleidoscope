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

%token TOK_RIGHTCURLY TOK_LEFTCURLY TOK_COMMA TOK_FILE TOK_AT TOK_DOLLAR
%token TOK_RIGHTBRACKET TOK_LEFTBRACKET TOK_ARROW TOK_BACK_ARROW TOK_LEFTPAREN TOK_RIGHTPAREN

%union {
  Node *node;
  ObjectNode *object;
  EntryNode *entry;
  std::vector<EntryNode*> *entryVec;

  RelationRestrictionsNode *r_restrictions;
  RelationRestrictionNode *r_restriction;
  std::vector<RelationRestrictionNode*> *r_restriction_vec;
  RelationSetNode *r_set;
  RelationNode *r_relation;
  StringNode *r_string;

  double number;
  std::string *str;

  std::string *string;
  int token;



  //frp
  FRPStatementNode *frpsmt;
  FRPSimpleExprNode *snp;
  std::vector<FRPSimpleExprNode*> *simple_expr_vector;
}

%token <number> TOK_NUMBER;
%token <str> TOK_STRING TOK_KEY TOK_J TOK_L TOK_F TOK_S TOK_EQUAL TOK_COLON;

%type <object> start object;
%type <entry> entry; 
%type <node> value restriction_val;
%type <entryVec> entries;

%type <r_relation> relation_expr;
%type <r_restriction> restriction;
%type <r_restrictions> restrictions;
%type <r_restriction_vec> restriction_list;
%type <r_set> operation_set set;
%type <r_string> relation_rule;
%type <str> restriction_op;

//frp stuff
%type <snp> frp_simple_expr;
%type <frpsmt> frp_statement;
%type <simple_expr_vector> frp_exprlist;

%start start

%%

start             : entries              { root = new ObjectNode(*$1); }
                  | object               { root = $1; }
                  ;

/* Basic JSON rules with a couple simplifying twists */
object            : TOK_LEFTCURLY entries TOK_RIGHTCURLY         { $$ = new ObjectNode(*$2); }
                  | TOK_KEY TOK_LEFTCURLY entries TOK_RIGHTCURLY { std::string type("type"); 
                                                                   std::string value("\"" + *$1 + "\"");
                                                                   $3->push_back(new EntryNode(type,new StringNode(value))); 
                                                                   $$ = new ObjectNode(*$3); }
                  | TOK_LEFTCURLY TOK_RIGHTCURLY                 { $$ = new ObjectNode(); }
                  | TOK_KEY                                      { std::string type("type");
                                                                   std::string value("\""+ *$1 + "\"");
								   std::vector<EntryNode*> *entries = new std::vector<EntryNode*>();
								   entries->push_back(new EntryNode(type,new StringNode(value)));
                                                                   $$ = new ObjectNode(*entries); }
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
                  | relation_expr       { $$ = $1; }
                  | frp_statement       { $$ = $1; }
                  ; 


/* Relation expression rules */
relation_expr     : relation_rule restrictions operation_set { $$ = new RelationNode($1, $2, $3); }
                  ;

/* RESTRICTIONS */
restrictions      : TOK_LEFTBRACKET restriction_list TOK_RIGHTBRACKET { $$ = new RelationRestrictionsNode(*$2); } 
                  | TOK_LEFTBRACKET TOK_RIGHTBRACKET                  { $$ = new RelationRestrictionsNode(); } 
                  ;

restriction_list  : restriction                            { $$ = new std::vector<RelationRestrictionNode*>(); $$->push_back($1); }
                  | restriction TOK_COMMA restriction_list { $3->push_back($1); $$ = $3; }
                  ;

restriction       : TOK_KEY restriction_op restriction_val      { $$ = new RelationRestrictionNode(*$1, *$2, $3); }
                  ;

restriction_op    : TOK_EQUAL           { $$ = $1; }
                  | TOK_COLON           { $$ = $1; }
                  ;

restriction_val   : TOK_STRING          { $$ = new StringNode(*$1); }
                  | TOK_NUMBER          { $$ = new NumberNode($1); }
                  ;

relation_rule     : TOK_S               { $$ = new StringNode(*$1); }
                  | TOK_F               { $$ = new StringNode(*$1); }
                  ;

/* OPERATION SETS */
operation_set     : TOK_LEFTPAREN set TOK_RIGHTPAREN  { $$ = $2; }
                  ;

set               : TOK_KEY TOK_ARROW TOK_KEY { $$ = new RelationSetNode(*$1, *$3); }
                  ;


/* 
 * BEGIN PARSING OF FRP EXPRESSIONS 
 */

frp_statement     : frp_expr {}
                  | TOK_KEY TOK_BACK_ARROW frp_expr {} 
                  ;

frp_expr          : frp_simple_expr {}
                  | frp_signet {}
                  ;

frp_signet        : TOK_LEFTPAREN frp_exprlist TOK_RIGHTPAREN TOK_ARROW frp_signet {}
                  | TOK_LEFTPAREN frp_exprlist TOK_RIGHTPAREN {}

frp_exprlist      : frp_simple_expr                        { $$ = new std::vector<FRPSimpleExprNode*>(); $$->push_back($1); }
                  | frp_simple_expr TOK_COMMA frp_exprlist { $3->push_back($1); $$ = $3; }

frp_simple_expr   : TOK_L TOK_LEFTBRACKET TOK_STRING TOK_RIGHTBRACKET { $$ = new FRPSimpleExprNode(new JavascriptNode(*$3)); }
                  | TOK_AT TOK_KEY                                    { $$ = new FRPSimpleExprNode(new FRPAtNode(*$2)); }
                  | TOK_DOLLAR TOK_KEY                                { $$ = new FRPSimpleExprNode(new FRPDollarNode(*$2)); }
                  ;



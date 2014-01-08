
%{
#include <string.h>
#include "node.hpp"
#include "parser.hpp"

#define SAVE_TOKEN yylval.string = new std::string(yytext, yyleng)
#define SAVE_TOKEN_DOUBLE yylval.number = atof(yytext)
#define TOKEN(t) (yylval.token = t)
extern "C" {
  int yywrap() { return 1; }
}

%}

TOK_STRINGCON     (\"([^\\"\n]|\\[\\'"0nt])*\")

%%
"//".* ;
[ \t\n] ;

"f"                   return TOKEN(TOK_FILE);
[a-zA-Z][a-zA-Z0-9_]* SAVE_TOKEN; return TOK_KEY;
[0-9]+                SAVE_TOKEN_DOUBLE; return TOK_NUMBER;
{TOK_STRINGCON}       SAVE_TOKEN; return TOK_STRING;


"}"                   return TOKEN(TOK_RIGHTCURLY);
"{"                   return TOKEN(TOK_LEFTCURLY);
","                   return TOKEN(TOK_COMMA);
":"                   return TOKEN(TOK_COLON);
.                     printf("Unknown token\n"); yyterminate();

%%

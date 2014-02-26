
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
[ \t] ;
\n yylineno++;

"f"                   return TOKEN(TOK_FILE);
"S"                   SAVE_TOKEN; return TOK_S;
"F"                   SAVE_TOKEN; return TOK_F;
"J"                   SAVE_TOKEN; return TOK_J;
"L"                   SAVE_TOKEN; return TOK_L;
"@"                   SAVE_TOKEN; return TOK_AT;
"$"                   SAVE_TOKEN; return TOK_DOLLAR;

[a-zA-Z][a-zA-Z0-9_]* SAVE_TOKEN; return TOK_KEY;
-?[0-9]+              SAVE_TOKEN_DOUBLE; return TOK_NUMBER;
{TOK_STRINGCON}       SAVE_TOKEN; return TOK_STRING;

":"                   SAVE_TOKEN; return TOK_COLON;
"="                   SAVE_TOKEN; return TOK_EQUAL;
"->"                  return TOKEN(TOK_ARROW);
"<-"                  return TOKEN(TOK_BACK_ARROW);
"]"                   return TOKEN(TOK_RIGHTBRACKET);
"["                   return TOKEN(TOK_LEFTBRACKET);
"}"                   return TOKEN(TOK_RIGHTCURLY);
"{"                   return TOKEN(TOK_LEFTCURLY);
")"                   return TOKEN(TOK_RIGHTPAREN);
"("                   return TOKEN(TOK_LEFTPAREN);
","                   return TOKEN(TOK_COMMA);
.                     printf("Unknown token\n"); yyterminate();

%%


%{
#include <string.h>
#include "node.hpp"
#include "parser.hpp"

#define SAVE_TOKEN yylval.string = new std::string(yytext, yyleng)
#define TOKEN(t) (yylval.token = t)
extern "C" {
  int yywrap() { return 1; }
}

%}

TOK_STRINGCON     (\"([^\\"\n]|\\[\\'"0nt])*\")

%%
[ \t\n] ;

[a-zA-Z][a-zA-Z0-9_]* printf("Key: %s\n", yytext); SAVE_TOKEN; return TOK_KEY;
[0-9]+                printf("Num: %s\n", yytext); SAVE_TOKEN; return TOK_NUMBER;
{TOK_STRINGCON}       printf("Str: %s\n", yytext); SAVE_TOKEN; return TOK_STRING;


"}"                   printf("Curls2\n");  return TOKEN(TOK_RIGHTCURLY);
"{"                   printf("Curls1\n"); return TOKEN(TOK_LEFTCURLY);
","                   printf("Comma\n"); return TOKEN(TOK_COMMA);
":"                   printf("Colon\n"); return TOKEN(TOK_COLON);
.                     printf("Unknown token\n"); yyterminate();

%%

#include <iostream>
#include <stdio.h>
#include <sstream>
#include "node.hpp"

extern int yyparse();
extern ObjectNode *root;

int main() {
  yyparse();
  FILE *fp = fopen("dictionary.py", "w");
  std::stringstream ss;
  ss << *root;
  fprintf(fp, "d = %s\n", ss.str().c_str());
}

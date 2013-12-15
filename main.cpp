#include <iostream>
#include "node.h"

extern int yyparse();
extern ObjectNode *root;

int main() {
  yyparse();
  std::cout << root << std::endl;
  
}

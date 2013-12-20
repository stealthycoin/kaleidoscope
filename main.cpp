#include <iostream>
#include "node.hpp"

extern int yyparse();
extern ObjectNode *root;

int main() {
  yyparse();
  std::cout << *root << std::endl;
  
}

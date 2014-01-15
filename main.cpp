#include <iostream>
#include <stdio.h>
#include <string>
#include <sstream>
#include <fstream>
#include <streambuf>
#include "node.hpp"

extern int yyparse();
extern ObjectNode *root;

/* Read file into string. */
inline std::string slurp (const std::string& path) {
  std::ostringstream buf; 
  std::ifstream input (path.c_str()); 
  buf << input.rdbuf(); 
  return buf.str();
}

int main(int argc, char** argv) {
  yyparse();
  std::string preamble = slurp("/usr/local/lib/kaleidoscope/dictPreamble.py");
 
  FILE *fp = fopen("dictionary.py", "w");
  std::stringstream ss;
  ss << *root;
  fprintf(fp, "%sd = %s\n", preamble.c_str(), ss.str().c_str());
}

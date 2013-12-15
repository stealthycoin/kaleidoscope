#ifndef _PARSER_Y_
#define _PARSER_Y_

#include <string>
#include <vector>


class Node {
 public:
  virtual ~Node();
};

class StringNode : public Node {
 public:
  StringNode(std::string initial) { value = initial;}
  std::string value;
};

class NumberNode : public Node {
 public:
  NumberNode(double initial) { value = initial;}
  double value;
};

class EntryNode : public Node {
 public:
  EntryNode(std::string is, Node *iv) {key = is; value = iv;}
  std::string key;
  Node *value;
  
};

class ObjectNode : public Node {
 public:
  ObjectNode(std::vector<EntryNode> *initial) { entries = initial; }
  std::vector<EntryNode> *entries;
};


#endif

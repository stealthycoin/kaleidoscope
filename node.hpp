#ifndef _PARSER_Y_
#define _PARSER_Y_

#include <string>
#include <vector>


class Node {
 public:
  virtual ~Node() {}
};

class StringNode : public Node {
 public:
  StringNode(std::string &value) : value(value) {}
  std::string value;
};

class NumberNode : public Node {
 public:
  NumberNode(double value) : value(value) {}
  double value;
};

class EntryNode : public Node {
 public:
  EntryNode(std::string &key, Node *value) : key(key), value(value) {}
  std::string key;
  Node *value;
  
};

class ObjectNode : public Node {
 public:
  ObjectNode(std::vector<EntryNode*> &entries) : entries(entries) {}
  std::vector<EntryNode*> entries;
};


#endif

#ifndef _PARSER_Y_
#define _PARSER_Y_
#include <iostream>

#include <string>
#include <sstream>
#include <vector>


class Node {
 public:
  virtual ~Node() {}
  virtual std::string show() const {return "nope";}
  friend std::ostream &operator<<(std::ostream &output, const Node &n);
};

class StringNode : public Node {
 public:
  StringNode(std::string &value) : value(value) {}
  std::string value;

  std::string show() const { return value; }
};

class NumberNode : public Node {
 public:
  NumberNode(double value) : value(value) {}
  double value;

  std::string show() const {
    std::stringstream ss;
    ss << value;
    return ss.str();
  }
};

class EntryNode : public Node {
 public:
  EntryNode(std::string &key, Node *value) : key(key), value(value) {}
  std::string key;
  Node *value;

  std::string show() const {
    std::stringstream ss;
    ss << key << " : " << value->show();
    return ss.str();
  }
};

class ObjectNode : public Node {
 public:
  ObjectNode(std::vector<EntryNode*> &entries) : entries(entries) {}
  std::vector<EntryNode*> entries;

  std::string show() const {
    std::stringstream ss;
    ss << "{";
    for (unsigned int i = 0 ; i < entries.size() ; i++) {
      ss << entries[i]->show() << " ";
    }
    ss << "}";
    return ss.str();
  }
};


#endif

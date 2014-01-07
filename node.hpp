#ifndef _PARSER_Y_
#define _PARSER_Y_
#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
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

class FileNode : public Node {
 public:
  FileNode(std::string &value) : value(value) {}
  std::string value;

  std::string show() const {
    std::stringstream ss;
    std::string filepath = std::string(value);
    std::ifstream in(filepath.substr(1,filepath.length()-2).c_str());
    
    if (in.fail()) {
      ss << "\"File " << filepath.substr(1,filepath.length()-2) << " not found\"";
    }
    else {
      std::string line;
      ss << "\"";
      while (std::getline(in,line)) {
	//replace all " with \"
	std::size_t loc = -2;
	while ((loc = line.find("\"", loc+2)) != std::string::npos) {
	  std::cout << line << "\n";
	  line = line.substr(0,loc) + "\\" + line.substr(loc);
	}

	ss << line << "\\n";
      }
      ss << "\"";
    }
    return ss.str();
  }
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
    ss << "\"" << key << "\"" << ":" << value->show();
    return ss.str();
  }
};

class ObjectNode : public Node {
 public:
  ObjectNode() { entries = std::vector<EntryNode*>(0); }
  ObjectNode(std::vector<EntryNode*> &entries) : entries(entries) {}
  std::vector<EntryNode*> entries;

  std::string show() const {
    std::stringstream ss;
    bool first = true;
    ss << "{";
    for (unsigned int i = 0 ; i < entries.size() ; i++) {
      if (first) first = false;
      else ss << ",";
      ss << entries[i]->show();
    }
    ss << "}";
    return ss.str();
  }
};


#endif

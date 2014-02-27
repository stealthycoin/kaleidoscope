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
    for (int i = entries.size() - 1 ; i >= 0 ; i--) {
      if (first) first = false;
      else ss << ",";
      ss << entries[i]->show();
    }
    ss << "}";
    return ss.str();
  }
};


//Nodes for building relation expressions

class RelationSetNode : public Node {
public:
  RelationSetNode(std::string &app, std::string &model) : app(app), model(model) {}
  std::string app, model;

  std::string show() const {
    std::stringstream ss;
    
    ss << "R_Set(\"" << app << "\",\"" << model << "\")";

    return ss.str();
  }
};


class RelationRestrictionNode : public Node {
public:
  RelationRestrictionNode(std::string &key, std::string &op, Node *value) : key(key), op(op), value(value) {}
  std::string key, op;
  Node *value;

  std::string show() const {
    std::stringstream ss;
    
    ss << "(\"" << key << "\",\"" << op << "\"," << value->show() << ")";

    return ss.str();
  }
};

class RelationRestrictionsNode : public Node {
public:
  RelationRestrictionsNode() { restrictions = std::vector<RelationRestrictionNode*>(0); }
  RelationRestrictionsNode(std::vector<RelationRestrictionNode*> &restrictions) : restrictions(restrictions) {}
  std::vector<RelationRestrictionNode*> restrictions;

  std::string show() const {
    std::stringstream ss;
    bool first = true;
    ss << "R_Restrictions([";
    for (int i = restrictions.size() - 1; i >= 0; i--) {
      if (first) first = false;
      else ss << ",";
      ss << restrictions[i]->show();
    }
    ss << "])";
    return ss.str();
  }
};

class RelationNode : public Node {
public:
  RelationNode(StringNode *type, RelationRestrictionsNode *restrictions, RelationSetNode *set) : type(type), restrictions(restrictions), set(set) {}
  StringNode *type;
  RelationRestrictionsNode *restrictions;
  RelationSetNode *set;

  std::string show() const {
    std::stringstream ss;

    ss << "R_Expr(R_Type(\"" << type->show() << "\")," << restrictions->show() << ","<< set->show() << ")";

    return ss.str();
  }
};


/*
 * Begin FRP nodes
 */

class JavascriptNode : public Node {
public:
  JavascriptNode(std::string &str) : str(str) {}

  std::string str;

  std::string show() const {
    return "";
  }
};

class FRPAtNode : public Node {
public:
  FRPAtNode(std::string &str) : str(str) {}

  std::string str;

  std::string show() const {
    return "";
  }
};

class FRPDollarNode : public Node {
public:
  FRPDollarNode(std::string &str) : str(str) {}

  std::string str;

  std::string show() const {
    return "";
  }
};


class FRPSimpleExprNode : public Node {
public:
  FRPSimpleExprNode(JavascriptNode *js) : js(js), d(NULL), a(NULL) {}
  FRPSimpleExprNode(FRPDollarNode *d) : d(d), js(NULL), a(NULL) {}
  FRPSimpleExprNode(FRPAtNode *a) : a(a), d(NULL), js(NULL) {}

  FRPDollarNode *d;
  FRPAtNode *a;
  JavascriptNode *js;

  std::string show() const {
    return "";
  }
};


class FRPExpressionNode : public Node {
public:
  FRPExpressionNode(std::vector<std::vector<FRPSimpleExprNode*>*> *signals) : signals(signals), expr(NULL) {}
  FRPExpressionNode(FRPSimpleExprNode *expr) : signals(NULL), expr(expr) {}
  
  std::vector<std::vector<FRPSimpleExprNode*>*>* signals;
  FRPSimpleExprNode *expr;

  std::string show() const {
    return "";
  }

};

class FRPStatementNode : public Node {
public:
  FRPStatementNode(FRPExpressionNode *expr) : varName(""), expr(expr) {}
  FRPStatementNode(std::string &varName, FRPExpressionNode *expr) : varName(varName), expr(expr) {}
  
  FRPExpressionNode *expr;
  std::string varName;

  std::string show() const {
    return "";
  }
};


#endif

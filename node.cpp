#include "node.hpp"

std::ostream &operator<<(std::ostream &output, const Node &node) {
  output << node.show() << std::endl;
  return output;
}

from typing import List

class TreeInterface:
  def validNode(self, node):
    '''return if node is in the tree'''
  def hasChildren(self, node: str) -> bool:
    '''does a given node have children'''
    pass
  def getChildren(self) -> List[str]:
    '''return list of children for current node'''
    pass


class TocTree(TreeInterface):
  def __init__(self, toc: dict):
    self.toc = toc

  def validNode(self, node):
    # quick incomplete check
    if self.hasChildren(node):
      return True
    # slow complete check
    for children in self.getChildren(node):
      if node in children:
        return True
    return False

  def hasChildren(self, node):
    return node in self.toc
  
  def getChildren(self, node):
    if self.hasChildren(node):
      return self.toc[node]
    else:
      return []

  def getToc(self):
    return self.toc


def traverseTree(tree: TreeInterface, start_node, nodeCheck, callback):
# in order recursive traversal
# callback runs on each node if nodeCheck is True
  def recurse(tree, node, depth, callback):
    if nodeCheck(node):
      callback(node, depth)
    
    if not tree.hasChildren(node):
      return

    for child in tree.getChildren(node):
      recurse(tree, child, depth + 1, callback)
  recurse(tree, start_node, 0, callback)

def getListOfAllNodes(tree: TreeInterface):
# unique list of all nodes in tree in order
  def makeListUnique(list):
  # preserves order
    seen = set()
    return [x for x in list if not (x in seen or seen.add(x))]

  nodes = []
  def addToList(node, depth=0):
    if node != 'root':
      nodes.append(node)
  traverseTree(tree, 'root', (lambda x: True), addToList)
  return makeListUnique(nodes)

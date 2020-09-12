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

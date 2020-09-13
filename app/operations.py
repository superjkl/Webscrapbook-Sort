from natsort import natsorted, ns
from app.tree import TreeInterface, TocTree
from app.data import Toc, Metadata, FolderIdToTitle, FolderTitleToId, writeTOC

# printing folders
###############################################################################

def isFolderById(id_val):
  return id_val in FolderIdToTitle()


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


def printFolders():
  tree = TocTree(Toc())

  def print_folder(id_val, depth):
    print("  " * depth + " " + FolderIdToTitle()[id_val] )

  traverseTree(tree, 'root', isFolderById, print_folder)

###############################################################################


# sorting folders
###############################################################################

def isFolderByTitle(utitle):
  return utitle in FolderTitleToId()

def sortFolder(utitle, sort_key, sort_direction, recursive=''):
  tree = TocTree(Toc())
  
  def get_id(utitle):
    return FolderTitleToId()[utitle]

  if not isFolderByTitle(utitle):
    print('This idname is not a folder in the tree')
    return

  sort_direction = False if sort_direction == 'a' else True
  sortTreeAtNode(tree, get_id(utitle), sort_key, sort_direction, recursive)
  writeTOC(tree.getToc())

def sortTreeAtNode(tree, node, sort_key, sort_direction, recursive):
  metadata = Metadata()

  def sortCurrentFolder(node, depth=0):
    sortFolderById(tree.getToc(), metadata, node, sort_key, sort_direction)

  def hasChildren(node):
    return tree.hasChildren(node)
  
  if not recursive:
    sortCurrentFolder(node)
  else:
    traverseTree(tree, node, hasChildren, sortCurrentFolder)




# default natural sort case insensitive
def sortFolderById(toc, metadata, id, sort_key, sort_direction):
  toc[id] = natsorted(toc[id], key = lambda e : metadata[e][sort_key], alg=ns.IGNORECASE)
  if sort_direction:
    toc[id].reverse()

###############################################################################


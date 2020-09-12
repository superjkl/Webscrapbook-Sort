from natsort import natsorted, ns
from app.tree import TreeInterface, TocTree
from app.data import Toc, Metadata, FolderIdToTitle, FolderTitleToId, writeTOC

# printing folders
###############################################################################

#callback runs at each "node" or key in the dictionary and terminal values
#in order recursion
def traverseTree(tree: TreeInterface, start_node, nodeCheck, callback):
  def recurse(tree, node, depth, callback):
    if not tree.hasChildren(node):
      return

    for child in tree.getChildren(node):
      if nodeCheck(child):
        callback(child, depth)
      recurse(tree, child, depth + 1, callback)
  recurse(tree, start_node, 0, callback)


def printFolders():
  tree = TocTree(Toc())

  def is_folder(id_val):
    return id_val in FolderIdToTitle()

  def print_folder(id_val, depth):
    print("  " * depth + " " + FolderIdToTitle()[id_val] )

  traverseTree(tree, 'root', is_folder, print_folder)

###############################################################################


# sorting folders
###############################################################################

def sortFolder(utitle, sort_key, sort_direction, recursive=''):
  metadata = Metadata()
  toc = Toc()

  def is_folder(utitle):
    return utitle in FolderTitleToId()

  def get_id(utitle):
    return FolderTitleToId()[utitle]

  if not is_folder(utitle):
    print('This idname is not a folder in the tree')
    return

  sort_direction = False if sort_direction == 'ascending' else True
  sortFolderById(toc, metadata, get_id(utitle), sort_direction, sort_key)

  writeTOC(toc)

# default natural sort case insensitive
def sortFolderById(tree, metadata, id, sort_direction, sort_key):
  tree[id] = natsorted(tree[id], key = lambda e : metadata[e][sort_key], alg=ns.IGNORECASE)
  if sort_direction:
    tree[id].reverse()

###############################################################################


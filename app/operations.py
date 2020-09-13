from natsort import natsorted, ns
from app.tree import TreeInterface, TocTree, traverseTree
from app.data import Toc, Metadata, FolderIdToTitle, FolderTitleToId, writeTOC

# printing folders
###############################################################################

def isFolderById(id_val):
  return id_val in FolderIdToTitle()

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

def sortFolder(args):
  def get_id(utitle):
    return FolderTitleToId()[utitle]

  if not isFolderByTitle(args.folder):
    print('This idname is not a folder in the tree')
    return

  args.sort_dir = False if args.sort_dir == 'a' else True
  tree = TocTree(Toc())
  sortTreeAtNode(tree, get_id(args.folder), args.sort_key, args.sort_dir, args.recursive)
  writeTOC(tree.getToc())

def sortTreeAtNode(tree: TreeInterface, node, sort_key, sort_direction, recursive):
  metadata = Metadata()

  def sortCurrentFolder(node, depth=0):
    sortFolderById(tree.getToc(), metadata, node, sort_key, sort_direction)
  
  if not recursive:
    sortCurrentFolder(node)
  else:
    traverseTree(tree, node, tree.hasChildren, sortCurrentFolder)

def sortFolderById(toc, metadata, id, sort_key, sort_direction):
# default natural sort case insensitive
  toc[id] = natsorted(toc[id], key = lambda e : metadata[e][sort_key], alg=ns.IGNORECASE)
  if sort_direction:
    toc[id].reverse()

###############################################################################


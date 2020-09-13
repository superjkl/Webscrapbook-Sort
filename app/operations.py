from natsort import natsorted, ns
from app.tree import TreeInterface, TocTree, traverseTree
from app.data import Toc, Metadata, FolderIdToTitle, FolderTitleToId, writeTOC

# printing folders
###############################################################################

def isFolderById(id_val):
  return id_val in FolderIdToTitle()

def printFolders():
  def print_folder(id_val, depth):
    print("  " * depth + " " + FolderIdToTitle()[id_val] )

  traverseTree(TocTree(Toc()), 'root', isFolderById, print_folder)

###############################################################################


# sorting folders
###############################################################################

def isFolderByTitle(utitle):
  return utitle in FolderTitleToId()

def sortFolder(args):
  if not isFolderByTitle(args.folder):
    print('This idname is not a folder in the tree')
    return

  sortTreeAtNode(FolderTitleToId()[args.folder], args.sort_key, args.sort_dir, args.recursive)
  writeTOC(Toc())

def sortTreeAtNode(node, sort_key, sort_direction, recursive):
  def sortCurrentFolder(node, depth=0):
    sortFolderById(node, sort_key, sort_direction)
  
  if not recursive:
    sortCurrentFolder(node)
  else:
    traverseTree(TocTree(Toc()), node, TocTree(Toc()).hasChildren, sortCurrentFolder)

def sortFolderById(id, sort_key, sort_direction):
# default natural sort case insensitive
  toc = Toc()
  metadata = Metadata()
  sort_direction = False if sort_direction == 'a' else True

  toc[id] = natsorted(toc[id], key = lambda e : metadata[e][sort_key], alg=ns.IGNORECASE)
  if sort_direction:
    toc[id].reverse()

###############################################################################


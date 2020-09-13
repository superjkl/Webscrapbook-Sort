import os, json, glob, collections
from app.tree import TocTree, getListOfAllNodes
from app.common import findFile, removeSuffix, removePrefix, removeLines, failure, parseJSON, areListElementsUnique, makeMappingOneToOne, invertDictionaryMap

TOC_FILE  = str("tree/toc.js")
TOC_GLOB  = str("tree/toc*.js")
META_FILE = str("tree/meta.js")
META_GLOB = str("tree/toc*.js")

FILE_COMMENT = "/** \n * Feel free to edit this file, but keep data code valid JSON format.\n */\n"
TOC_PREFIX   = "scrapbook.toc("
META_PREFIX  = "scrapbook.meta("
TOC_SUFFIX   = ")"
META_SUFFIX  = TOC_SUFFIX



def validCWD(dir):
# is cwd a scrapbook directory with necessary files
  def setCWD(dir):
    if dir:
      os.chdir(dir)

  def findToc():
    global TOC_FILE
    TOC_FILE = findFile(TOC_FILE, TOC_GLOB)
    return TOC_FILE

  def findMeta():
    global META_FILE
    META_FILE = findFile(META_FILE, META_GLOB)
    return META_FILE

  setCWD(dir)
  try:
    os.path.isdir('./tree')
  except:
    failure('Current working directory is not a scrapbook directory')

  toc = findToc()
  meta = findMeta()
  if not toc or not meta:
    failure('Current working directory is not a scrapbook directory')
  else:
    print('')
    print("Using files:")
    print('-----------------------------')
    print("  meta: " + meta)
    print("   toc: " + toc)
    print("\n")

def writeToc(toc):
  def backupToc():
    try:
      os.rename(TOC_FILE, TOC_FILE + '.bak')
    except:
      print(TOC_FILE + " backup already exists")

  def writeNewToc(toc):
    with open(TOC_FILE, "w") as file:
      json_string = FILE_COMMENT + TOC_PREFIX + json.dumps(toc) + TOC_SUFFIX
      file.write(json_string)
  
  backupToc()
  writeNewToc(toc)

# Toc and Metadata
###############################################################################
# Singleton classes to get toc and meta

class Toc(dict):
  @staticmethod
  def loadToc():
    def preprocess(string):
      return removeSuffix(
                removePrefix(
                  removeLines(string, 3), TOC_PREFIX), TOC_SUFFIX)
    return parseJSON(TOC_FILE, preprocess)

  _instance = None
  def __new__(cls):
      if cls._instance is None:
          cls._instance = cls.loadToc()
      return cls._instance

class Metadata(dict):
  @staticmethod
  def loadMetadata():
    def preprocess(string):
      return removeSuffix(
                removePrefix(
                  removeLines(string, 3), META_PREFIX), META_SUFFIX)
    return parseJSON(META_FILE, preprocess)

  _instance = None
  def __new__(cls):
      if cls._instance is None:
          cls._instance = cls.loadMetadata()
      return cls._instance

def getMetaEntry(id_val):
  return Metadata()[id_val]

###############################################################################


# FolderIdToTitle and FolderTitleToId
###############################################################################

class FolderIdToTitle(dict):
  @staticmethod
  def loadFolderIdToTitle():
  # make list of unique titles to associate with ids
    def getFolderIds():
      ids = getListOfAllNodes(TocTree(Toc()))
      if not areListElementsUnique(ids):
        failure('Ids in toc are not unique')
      return list(filter(lambda id_val: getMetaEntry(id_val)['type'] == 'folder', ids))
    
    folders = getFolderIds()
    folder_id_to_title = collections.OrderedDict({ id_val:getMetaEntry(id_val)['title'] for id_val in folders })
    # add implicit root folder (assumes no other folder can get the id of root)
    folder_id_to_title['root'] = 'root'
    folder_id_to_title.move_to_end('root', last=False)

    # (id) -> (unique title) dictionary
    makeMappingOneToOne(folder_id_to_title)
    return dict(folder_id_to_title)

  _instance = None
  def __new__(cls):
      if cls._instance is None:
          cls._instance = cls.loadFolderIdToTitle()
      return cls._instance

class FolderTitleToId(dict):
  _instance = None
  def __new__(cls):
      if cls._instance is None:
          cls._instance = invertDictionaryMap(FolderIdToTitle())
      return cls._instance

def isFolderByTitle(utitle):
  return utitle in FolderTitleToId()

def isFolderById(id_val):
  return id_val in FolderIdToTitle()

def getFolderId(utitle):
  return FolderTitleToId()[utitle]

def getFolderTitle(id_val):
  return FolderIdToTitle()[id_val]

###############################################################################
import os, sys, json, glob, collections
from app.tree import TocTree, getListOfAllNodes

TOC_FILE = str("tree/toc.js")
TOC_GLOB = "tree/toc*.js"
META_FILE = str("tree/meta.js")
META_GLOB = "tree/toc*.js"


FILE_COMMENT = "/** \n * Feel free to edit this file, but keep data code valid JSON format.\n */\n"
TOC_PREFIX = "scrapbook.toc("
META_PREFIX = "scrapbook.meta("
TOC_SUFFIX = ")"
# META_SUFFIX = ")"

def failure(fail_message):
  print(fail_message)
  sys.exit()

def getCWD():
  return os.path.realpath(os.getcwd())

def findFile(file, glob_val):
  cwd = getCWD()
  # default name in default location
  if os.path.isfile(cwd + '/' + file):
      return file
  else:
    possible_files = glob.glob(glob_val)
    if possible_files:
      # TODO: allow choice of file so return list
      return possible_files[0]
    else:
      return ""

def findToc():
  global TOC_FILE
  TOC_FILE = findFile(TOC_FILE, TOC_GLOB)
  return TOC_FILE

def findMeta():
  global META_FILE
  META_FILE = findFile(META_FILE, META_GLOB)
  return META_FILE

def validCWD():
# is cwd a scrapbook directory with necessary files
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

# Toc and Metadata
###############################################################################

# Singleton classes to get toc and meta

def loadToc():
  return parseJSON(TOC_FILE)

class Toc(dict):
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = loadToc()
        return cls._instance

def loadMetadata():
  return parseJSON(META_FILE)

class Metadata(dict):
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = loadMetadata()
        return cls._instance

def getMetaEntry(id_val):
  return Metadata()[id_val]

###############################################################################


# FolderIdToTitle and FolderTitleToId
###############################################################################

def areListElementsUnique(l):
  return len(l) == len(set(l))

def makeMappingOneToOne(mapping):
  range_occurrences = dict()
  for key, val in mapping.items():
    if val in range_occurrences:
      range_occurrences[val] += 1
    else:
      range_occurrences[val] = 0
    mapping[key] = val + ( "" if not range_occurrences[val] else "-" + str(range_occurrences[val]) )

def loadFolderIdToTitle():
# make list of unique titles to associate with ids
# TODO: return ids in order of table of contents
  
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

class FolderIdToTitle(dict):
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = loadFolderIdToTitle()
        return cls._instance

def invertDictionaryMap(dictionary):
  return {v: k for k, v in dictionary.items()}

class FolderTitleToId(dict):
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = invertDictionaryMap(FolderIdToTitle())
        return cls._instance

###############################################################################


# string functions
###############################################################################

def removePrefix(text, prefix):
  if text.startswith(prefix):
        return text[len(prefix):]
  return text

def removeSuffix(text, suffix):
  if text.endswith(suffix):
        return text[:-1 * len(suffix)]
  return text

def removeLines(s, count):
  s = s.split('\n', count)[-1]
  
  # file may have a single line left not terminated by a newline
  #if s.find('\n') == -1:
  #    return ''
  return s

def parseJSON(filename):
  data = {}
  with open(filename) as file:
    json_string = file.read()
    json_string = removeLines(json_string, 3)
    json_string = removePrefix(json_string, TOC_PREFIX)
    json_string = removePrefix(json_string, META_PREFIX)
    json_string = removeSuffix(json_string, TOC_SUFFIX)
    try:
      data = json.loads(json_string)
    except:
      failure('Could not parse')
  return data

def writeTOC(tree):
  #backup old toc
  try:
    os.rename('toc.js', 'toc.js.bak')
  except:
    print("toc.js backup already exists")
  #write new toc
  with open("toc.js", "w") as file:
    json_string = FILE_COMMENT + TOC_PREFIX + json.dumps(tree) + TOC_SUFFIX
    file.write(json_string)

###############################################################################
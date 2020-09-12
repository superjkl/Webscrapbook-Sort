import os, sys, json, glob

TOC_FILE = str("tree/toc.js")
TOC_GLOB = "tree/toc*.js"
META_FILE = str("tree/meta.js")
META_GLOB = "tree/toc*.js"


FILE_COMMENT = "/** \n * Feel free to edit this file, but keep data code valid JSON format.\n */\n"
TOC_PREFIX = "scrapbook.toc("
META_PREFIX = "scrapbook.meta("
TOC_SUFFIX = ")"
# META_SUFFIX = ")"

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
    print("Using files:")
    print("  meta: " + meta)
    print("   toc: " + toc)
    print("-----------------------------")
    print("\n")

def failure(fail_message):
    print(fail_message)
    sys.exit()


# Toc and Metadata
###############################################################################

# Singleton classes to get toc and meta

def loadToc():
# TODO:fix so globs to use toc*.js and meta*.js
  return parseJSON(TOC_FILE)

class Toc(dict):
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = loadToc()
        return cls._instance

def loadMetadata():
# TODO:fix so globs to use toc*.js and meta*.js
  return parseJSON(META_FILE)

class Metadata(dict):
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = loadMetadata()
        return cls._instance

###############################################################################


# FolderIdToTitle and FolderTitleToId
###############################################################################


def loadFolderIdToTitle():
# make list of unique titles to associate with ids
# TODO: return ids in order of table of contents
  metadata = Metadata()
  tree_folders = dict(filter(lambda e: e[1]['type'] == 'folder', metadata.items()))
  
  # get [(id, title), ...]
  # add implicit root folder (assumes no other folder can get the id of root)
  id_and_titles = [(k,v['title']) for (k,v) in tree_folders.items() ]
  id_and_titles.insert(0, ('root','root'))
  
  # creating (id) -> (unique title) dictionary
  titles = dict()
  id_to_utitle = dict()
  for id_val, title in id_and_titles:
    if title in titles:
      titles[title] += 1
    else:
      titles[title] = 0
    title_occurences = titles[title]
    id_to_utitle[id_val] = title + ( "" if not title_occurences else "-" + str(title_occurences) )
  return id_to_utitle

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
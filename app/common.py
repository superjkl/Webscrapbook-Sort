import sys, os, glob, json

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

# collection functions
###############################################################################

def invertDictionaryMap(dictionary):
  return {v: k for k, v in dictionary.items()}

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

def parseJSON(filename, preprocessing):
  data = {}
  with open(filename) as file:
    json_string = preprocessing(file.read())
    try:
      data = json.loads(json_string)
    except:
      failure('Could not parse')
  return data

###############################################################################

#!/usr/bin/python3

# Run this script in the scrapbook directory you wish to sort

# get* functions are singletons for load* functions

import sys, argparse
from app.data import validCWD
from app.operations import printFolders, sortFolder

# Start script
###############################################################################
validCWD()
args = sys.argv[1:]

'''
options
  folders - prints folders
  sort 
    arg: folder idname
    options: title, create, modify, source, etc.
    options: ascending descending
    options: recursive [nonrecursive]

'''
if len(args) > 0:
  operation = args.pop(0)
  if operation == 'folders':
    printFolders()
  elif operation == 'sort':
    if len(args) >= 2:
      utitle = args.pop(0)
      #check valid utitle
      
      sort_key = args.pop(0)
      #check valid sort key
      
      sort_direction = args.pop(0) if len(args) >= 1 else 'ascending'
      #check valid direction
      
      recursive = args.pop(0) if len(args) >= 1 else ''
      #check valid recursive
        
      sortFolder(utitle, sort_key, sort_direction, recursive)
  else:
    print('Invalid operation')
else:
  print('No operation specified')














# the key to sort by from metadata
# options: title, create, modify, source
##sort_key = sys.argv[1:]


# options: ascending descending
##order = sys.argv[1:]


'''
verify function - runs to confirm changes before writing them
check if same number of things in toc.js
check same number of things in folder in toc.js
check every id in toc.js exists in meta.js
'''
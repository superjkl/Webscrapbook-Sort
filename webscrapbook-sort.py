#!/usr/bin/python3

# Run this script in the scrapbook directory you wish to sort

import sys, argparse
from app.data import validCWD, failure
from app.operations import printFolders, sortFolder, isFolderByTitle

# commands
###############################################################################

def folders(args):
  printFolders()

def sortValidation(args):
  if not isFolderByTitle(args.folder):
    failure('ERROR: Folder given does not exist')

def sortConfimation(args):
  print('Sort options'\
  '\n-----------------------------\n'\
  '   folder: ' + args.folder + '\n'\
  '      key: ' + args.sort_key + '\n'\
  '      dir: ' + args.sort_dir + '\n'\
  'recursive: ' + str(args.recursive) + '\n'\
  '\n'\
  'This operation cannot be reversed (your original file will be moved)\n'\
  'Type \'yes\' to sort with these options:', end=' ')
  if input() == "yes":
    pass
  else:
    failure("Sort cancelled")
  pass

def sort(args):
  sortValidation(args)
  sortConfimation(args)
  sortFolder(args.folder, args.sort_key, args.sort_dir, args.recursive)
  pass

# Start script
###############################################################################

parser = argparse.ArgumentParser(description='Tool for sorting webscrapbook folders.')
subparsers = parser.add_subparsers(help='sub-command help')

# folders command
folders_parser = subparsers.add_parser('folders', aliases=['p'], help='print unique titles')
folders_parser.set_defaults(func=folders)

# sort command
sort_parser = subparsers.add_parser('sort', aliases=['s'], help='sort a given directory')
sort_parser.set_defaults(func=sort)
sort_parser.add_argument('folder',
                    help='unique title given by folders command')
sort_parser.add_argument('sort_key',
                    choices=['title','create', 'modify', 'source', 'comment'],
                    help='metadata key to sort on')
sort_parser.add_argument('sort_dir',
                    nargs='?',
                    choices=['a','d'],
                    default='a',
                    help='direction of sort ascending or descending')
sort_parser.add_argument('recursive',
                    choices=[True,False],
                    nargs='?',
                    type=bool,
                    default=False,
                    help='recursively sort child directories')


args = parser.parse_args()
validCWD()
args.func(args)


'''
verify function - runs to confirm changes before writing them
check if same number of things in toc.js
check same number of things in folder in toc.js
check every id in toc.js exists in meta.js
'''

'''
say number of things to be sorted
say number of things sorted

before and after sort report

if mismatch say oops error restore backup file by renaming it to original filename
'''
# webscrapbook-sort
Python cli tool for sorting webscrapbook folders.

## Usage:
### show folders

    ./webscrapbook-sort.py folders

### sort folder
first run the folders command to find a folder to sort

    ./webscrapbook-sort.py [-h] [-d directory] sort <folder_name> <sort_key> [sort_direction] [-r]

- -h            : help
- folder_name   : name of the folder to sort (be careful to use the names given by the folders command for the unique folder name)
- sort_key      : title, modify, create, source, comment
- sort_direction: a, d (ascending or descending)
- -r            : recursively sort directory

ex.

    ./webscrapbook-sort.py sort myfolder-1 title
    ./webscrapbook-sort.py -d ~/webscrapbook/ sort myfolder modify

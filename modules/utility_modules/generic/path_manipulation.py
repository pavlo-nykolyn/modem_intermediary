# Author: Pavlo Nykolyn
# Last modification date: 06/07/2025

"""
Collects functions that manipulate path components
"""

from utility_modules.generic import token

def modify_path(path) :
   """
   modifies the delimiter between path components. The modification
   depends on the operating system that hosts the program
   """
   if token == 'Windows' :
      path = path.replace('/', '\\')
   elif token == 'Linux' :
      path = path.replace('\\', '/')
   return path

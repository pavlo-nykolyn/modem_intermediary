# Author: Pavlo Nykolyn
# Last modification date: 19/01/2025
"""
Implements the Logger class
"""

import sys
import os.path
from utility_modules.timestamp.ts_format import get_current_ts

class Logger :
   o_stream = sys.stdout # output stream
   l_st = False # logger status
   def __init__(self, o_path=None, o_mode='a') :
      """
      Constructor of a Logger instance.
      |** INPUT PARAMETERS **|
      o_path -> absolute path of the output stream;
      o_mode -> message storage mode.
      |** DEFAULT BEHAVIOUR **|
      When o_path is not specified, sys.stdout will be used;
      the default mode is append.
      """
      if o_path :
         # currently, only text mode is allowed
         if (o_mode != 'a' or
             o_mode != 'w') :
            self.store_message('unsupported file mode', prefix='[ERR]', parent_class=str(self.__class__), f_ts=True)
            self.store_message('{} will not be opened'.format(o_path), prefix='[INF]', parent_class=str(self.__class__), f_ts=True)
            return
         if os.path.isdir(o_path) :
            self.o_stream = open(o_path, o_mode)
            l_st = True
   def store_message(self, *comp, prefix='', parent_class='', f_ts=False, sep=' ', trail_ch='\n') :
      """
      Creates a message that will be appended to a log stream. 
      |** INPUT PARAMETERS **|
      comp -> sequence of sub-strings that will be appended to the message;
      parent_class -> name of the parent class
      prefix -> first sub-string of the message;
      f_ts -> a boolean flag that enables/disables the generation of a time-stamp. The
              latter will be added to the message after prefix but, before the first
              element of comp;
      sep -> a string that separates two sub-strings within the message;
      trail_ch -> last character of the message;
      """
      source_str = prefix
      if len(parent_class) :
         source_str += sep + '[' + parent_class + ']'
      if f_ts :
         source_str += sep + get_current_ts()
      for elem in comp :
         source_str += sep + elem
      print(source_str, end=trail_ch, file=self.o_stream)

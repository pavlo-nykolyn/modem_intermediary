# Author: Pavlo Nykolyn
# Last modification date: 07/07/2025

"""
provides the Stream_configurator class. The latter implements
an interface that can be inherited by other classes that obtain
configuration data from a stream
"""

from utility_modules.exceptions.abstractEntity import AbstractEntity
from utility_modules.generic.path_manipulation import modify_path

class Stream_configurator :
   def __init__(self,
                file_path,
                aLogger) :
      """
      ||**ATTRIBUTES**||
      file_path -> path of the file containing configuration data;
      aLogger -> instance of the Logger class
      """
      self.file_path = modify_path(file_path)
      self.aLogger = aLogger

   def retrieve(self) :
      """
      attempts the retrieval of the configuration data;
      ||**INSTANCE ATTRIBUTE**||
      blob -> the data received from the input stream;
      """
      raise AbstractEntity('attempting to use the abstract method {}'.format(Stream_configurator.retrieve.__name__))

   def parse(self) :
      """
      parses the blob retrieved from the configuration file
      """
      raise AbstractEntity('attempting to use the abstract method {}'.format(Stream_configurator.parse.__name__))

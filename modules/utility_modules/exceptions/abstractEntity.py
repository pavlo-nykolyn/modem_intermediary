# Author: Pavlo Nykolyn
# Last modification date: 07/07/2025

"""
Defines the AbstractEntity exception an its sub-classes
"""

class AbstractEntity(Exception) :
   pass

class AbstractClass(AbstractEntity) :
   """
   an attempt at using an abstract class has occurred
   """
   pass

class AbstractMethod(AbstractEntity) :
   """
   an attempt at using an abstract method has occurred
   """
   pass

class AbstractFunction(AbstractEntity) :
   """
   an attempt at using an abstract function has occurred
   """
   pass

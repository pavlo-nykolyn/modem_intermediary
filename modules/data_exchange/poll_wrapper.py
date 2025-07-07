# Author: Pavlo Nykolyn
# Last modification date: 24/06/2025

"""
Defines a very simple class that wraps poll operations on
a single file descriptor
"""

from select import poll, POLLIN, POLLOUT, POLLHUP, POLLERR

class Poll_wrapper :
   # the sequence of supported operation types
   operation_types = ('read', # data available in the input buffer associated with the file descriptor
                      'write' # data available in the output buffer associated with the file descriptor
                     )
   # poll failure bit set
   failure_bitset = POLLHUP | POLLERR

   def __init__(self,
                operation_type,
                poll_timeout,
                descriptor) :
      """
      ||**INPUT PARAMETERS**||
      operation_type -> what kind of operation is to be monitored through the poll system call. Two
                        types are currently supported:
                        - read
                        - write
      ||**INSTANCE ATTRIBUTES**||
      success_bitset -> which bits need to be high in order to consider the poll operation successful;
      poll_timeout -> how many milliseconds have to expire before the poll is considered unsuccessful;
      descriptor -> monitoring descriptor;
      """
      if operation_type == Poll_wrapper.operation_types[0] :
         self.success_bitset = POLLIN
      elif operation_type == Poll_wrapper.operation_types[1] :
         self.success_bitset = POLLOUT
      self.instance = poll()
      self.instance.register(descriptor,
                             self.success_bitset | Poll_wrapper.failure_bitset)
      self.poll_timeout = poll_timeout
      self.descriptor = descriptor

   def perform(self) :
      """
      performs the poll
      ||**RETURN VALUE**||
      returns True if data is available and False otherwise
      """
      event = self.instance.poll(self.poll_timeout)
      polled = False
      if event :
         # the descriptor shall be the same of the one configured for the instance
         if (event[0][1] & self.success_bitset and
             event[0][0] == self.descriptor) :
            polled = True
      return polled

# Author: Pavlo Nykolyn
# Last modification date: 08/07/2025

"""
defines the Command_manipulator class, used to iterate the commands
that are to be executed
"""

from parsing.modem_response import Modem_response
from parsing.modem_command import Modem_command
from utility_modules.timestamp.ts_instance import create_instance_scts_naive

def getKey(anObj) :
   """
   generates the sort key is a formatted time-stamp
   """
   return create_instance_scts_naive(anObj['Service-center-timestamp'])

class Command_manipulator :
   # a sequence of error codes that may be returned to a client
   codes = (100, # an error condition occurred during response reception
            101, # an error condition occurred during response parsing
           )

   def __init__(self,
                request_instance,
                aLogger) :
      """
      ||**ATTRIBUTES**||
      request_instance -> an instance of the Modem_request class;
      aLogger -> an instance of the Logger class
      """
      self.request_instance = request_instance
      self.aLogger = aLogger

   def read_all_sms(self) :
      """
      retrieves all the SMS contained within a storage medium of the transmission equipment;
      ||**RETURN VALUE**||
      returns a dictionary that contains, at most, three keys:
              * filled-slots -> how many memory slots are currently in use;
              * maximum-slots -> the amount of available memory slots;
              * responses -> a sequence of formatted responses. Each element references a dictionary
      """
      collects = {}
      self.request_instance.dispatch(Modem_command.commands[1]) # used to obtain the maximum amount of memory slots
      self.request_instance.receive()
      read_response = self.request_instance.get_response()
      if read_response :
         response_instance = Modem_response(Modem_command.commands[1],
                                            self.aLogger)
         structured_response = response_instance.extract(read_response)
         # the key contains a sequence of nine elements. The last one holds the target value for the preferred
         # storage medium used to store received messages; the one next to the last one holds the current
         # amount of messages archived within the preferred storage medium
         collects['filled-slots'] = structured_response['data'][7]
         # there is no need to iterate the storage medium slots if no message is stored within it
         if collects['filled-slots'] :
            responses = []
            collects['maximum-slots'] = structured_response['data'][8]
            index_iterable = range(1, collects['maximum-slots'] + 1)
            response_instance = Modem_response(Modem_command.commands[0],
                                               self.aLogger)
            for idx in index_iterable :
               self.request_instance.dispatch(Modem_command.commands[0],
                                              parameter_sequence=str(idx))
               self.request_instance.receive()
               read_response = self.request_instance.get_response()
               if read_response :
                  structured_response = response_instance.extract(read_response)
                  if structured_response :
                     if self.aLogger :
                        self.aLogger.store_message('{} is the latest formatted data collection'.format(structured_response),
                                                   prefix='[INF]',
                                                   f_ts=True)
                     responses.append(structured_response)
            # sorting the responses in ascending order with respect to the service center time-stamp
            responses.sort(key=getKey)
            collects['responses'] = responses
            # deleting all the stored messages
            self.request_instance.dispatch(Modem_command.commands[6].format(idx))
            self.request_instance.receive()
      return collects

   def perform_command(self,
                       command,
                       parameter_sequence=None) :
      """
      performs a single operation through the given command.
      A result may be returned
      ||**INPUT PARAMETER**||
      parameter_sequence -> a character sequence that can be attached to the command before the latter gets dispatched
      """
      self.request_instance.dispatch(command,
                                     parameter_sequence=parameter_sequence)
      self.request_instance.receive()
      read_response = self.request_instance.get_response()
      structured_response = None
      if read_response :
         response_instance = Modem_response(Modem_command.commands[0],
                                            self.aLogger)
         structured_response = response_instance.extract(read_response)
         if structured_response :
            if self.aLogger :
               self.aLogger.store_message('{} is the latest formatted data collection'.format(structured_response),
                                          prefix='[INF]',
                                          f_ts=True)
      return structured_response

# Author: Pavlo Nykolyn
# Last modification date: 07/07/2025

"""
Implements the Modem_request class that enables data exchanges between a DTE
and a DCE
"""

from parsing.modem_command import Modem_command
from utility_modules.ascii.bArr_manager import byte_to_str, octet_to_str

def iterate_decoding(sequence) :
   """
   decodes a sequence of of elements referenced within a bytearray instance
   """
   decoded_sequence = ''
   for element in sequence :
      decoded_sequence += byte_to_str(element,
                                      None)

class Modem_request(Modem_command) :
   command_terminator = b'\x0D'
   decoded_command_terminator = octet_to_str(command_terminator)
   # currently, both the header and the footer are represented by:
   # - a command line termination character -> carriage return;
   # - a response formatting character -> line feed;
   header = b'\x0D\x0A'
   footer = b'\x0D\x0A'
   decoded_header = iterate_decoding(header)
   decoded_footer = iterate_decoding(footer)

   def __init__(self,
                port_handler,
                poll_wrapper_instance,
                aLogger) :
      """
      ||**ATTRIBUTES**||
      port_handler -> handler of the serial port;
      poll_wrapper_instance -> a Poll_wrapper instance;
      aLogger -> an instance of the Logger class;
      """
      self.port_handler = port_handler
      self.poll_wrapper_instance = poll_wrapper_instance
      self.aLogger = aLogger

   def remove_final_result_code(self) :
      """
      attempts to remove a final result code from a response. It is assumed that verbose mode
      is enabled on the mobile equipment
      """
      component = Modem_request.header + bytes('OK', 'ascii') + Modem_request.footer
      found_on = self.response.find(component)
      if found_on != -1  :
         if self.aLogger :
            self.aLogger.store_message('found {} at index {}'.format(component,
                                                                     found_on),
                                       prefix='[DEBUG]',
                                       f_ts=True)
         self.response = self.response[:found_on]

   def get_response(self) :
      """
      retrieves the response
      """
      return self.response

   def dispatch(self,
                command,
                parameter_sequence=None) :
      """
      dispatches an AT command;
      ||**INPUT PARAMETERS**||
      command -> what is to be requested;
      parameter_sequence -> a character sequence that can be attached to the last character of the command;
      ||**INSTANCE ATTRIBUTE**||
      command -> references the value of the input parameter;
      encoded_command -> an encoded byte sequence that represents the command;
      ||**RETURN VALUE**||
      returns the number of bytes that have been written
              ** ERROR CONDITION **
              None will be returned
      """
      bytes_written = None
      if command not in Modem_command.commands :
         if self.aLogger :
            self.aLogger.store_message('{} is not a valid command'.format(command),
                                       prefix='[ERR]',
                                       f_ts=True)
      else :
         for request in Modem_command.requests :
            if request['name'] == command :
               decoded_command = request['decoded']
               if ((request['name'] == 'read-SMS' or
                    request['name'] == 'delete-SMS') and
                   parameter_sequence) :
                  decoded_command = decoded_command.format(parameter_sequence)
               self.encoded_command = bytearray(decoded_command, 'ascii')
               message = self.encoded_command + Modem_request.command_terminator
               bytes_written = self.port_handler.write(message)
               if self.aLogger :
                  self.aLogger.store_message('{}{}'.format(decoded_command,
                                                           Modem_request.decoded_command_terminator),
                                             prefix='[MODEM_COMMAND]',
                                             f_ts=True)
               self.command = command
      return bytes_written

   def receive(self) :
      """
      ||**INSTANCE ATTRIBUTE**||
      response -> the received encoded response
      """
      self.response = b''
      decoded_response = ''
      polled = self.poll_wrapper_instance.perform()
      while polled :
         if self.aLogger :
            self.aLogger.store_message('available {} bytes'.format(self.port_handler.in_waiting),
                                       prefix='[DEBUG]',
                                       f_ts=True)
         octets = self.port_handler.read(self.port_handler.in_waiting)
         if self.aLogger :
            self.aLogger.store_message('received {} chunk'.format(octets),
                                       prefix='[DEBUG]',
                                       f_ts=True)
         self.response += octets
         for byte in octets :
            decoded_response += byte_to_str(byte,
                                            self.aLogger)
         polled = self.poll_wrapper_instance.perform()
      if (self.response and
          self.aLogger) :
         self.aLogger.store_message('{}'.format(decoded_response),
                                    prefix='[MODEM_RESPONSE]',
                                    f_ts=True)
      if (self.command != Modem_command.commands[-1] or
          self.command != Modem_command.commands[-2] or
          self.command != Modem_command.commands[-3]) :
         self.remove_final_result_code()

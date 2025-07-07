# Author: Pavlo Nykolyn
# Last modification date : 07/07/2025

"""
Implements the Serial_configurator class. It is used
to retrieve and parse configuration data related to
serial ports and can also be used to open them once
the configuration is available
"""

import yaml
from serial import Serial, FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS, PARITY_NONE, PARITY_EVEN, PARITY_ODD, PARITY_MARK, PARITY_SPACE, STOPBITS_ONE, STOPBITS_TWO, SerialException
from utility_modules.input.serial_stream.serial_parameters import baud_rates, parity_types, stop_bits, data_bits
from utility_modules.input.stream_configurator import Stream_configurator

class Serial_configurator(Stream_configurator) :
   # default configuration
   default = {'baud-rate' : 9600,
              'parity' : PARITY_NONE,
              'data-bits' : EIGHTBITS,
              'stop-bits' : STOPBITS_ONE
             }

   def translate_data_bits(self,
                           data_bits) :
      """
      attempts to translate the extracted number of data bits
      into an equivalent constant defined by pyserial. -1
      will be returned if no such value can be found
      """
      translated_value = -1
      if data_bits == 5 :
         translated_value = FIVEBITS
      elif data_bits == 6 :
         translated_value = SIXBITS
      elif data_bits == 7 :
         translated_value = SEVENBITS
      elif data_bits == 8 :
         translated_value = EIGHTBITS
      return translated_value

   def translate_stop_bits(self,
                           stop_bits) :
      """
      attempts to translate the extracted number of stop bits
      into an equivalent constant defined by pyserial. -1
      will be returned if no such value can be found
      """
      translated_value = -1
      if stop_bits == 1 :
         translated_value = STOPBITS_ONE
      elif stop_bits == 2 :
         translated_value = STOPBITS_TWO
      return translated_value

   def translate_parity_type(self,
                             parity) :
      """
      attempts to translate the extracted number of stop bits
      into an equivalent constant defined by pyserial. An empty
      string will be returned if no such value can be found
      """
      translated_value = ''
      if parity == 'none' :
         translated_value = PARITY_NONE
      if parity == 'even' :
         translated_value = PARITY_EVEN
      if parity == 'odd' :
         translated_value = PARITY_ODD
      if parity == 'mark' :
         translated_value = PARITY_MARK
      if parity == 'space' :
         translated_value = PARITY_SPACE
      return translated_value

   # all the check methods used the blob instance attribute
   def chk_numerical_parameter(self,
                               name,
                               supported_values) :
      """
      checks the extracted numerical parameter. If the value is not valid, -1 will be
      returned
      ||**INPUT VARIABLES**||
      name -> parameter name (as it appears within the extracted configuration);
      supported_values -> a sequence of supported values
      """
      value = -1
      try :
         value = int(self.blob['port']['configuration'][name])
      except ValueError :
         # the error condition is indicated by the value
         if self.aLogger :
            self.aLogger.store_message('{} is not an integer value'.format(self.blob['port']['configuration'][name]),
                                       prefix='[ERR]',
                                       f_ts=True)
      else :
         if value not in supported_values :
            if self.aLogger :
               self.aLogger.store_message('the value for {}, {}, is not supported'.format(name,
                                                                                          value),
                                          prefix='[ERR]',
                                          f_ts=True)
            value = -1
         else :
            if name == 'data-bits' :
               value = self.translate_data_bits(value)
            elif name == 'stop-bits' :
               value = self.translate_stop_bits(value)
      return value
      
   def chk_string_parameter(self,
                            name,
                            supported_values) :
      """
      checks the extracted string parameter. If the value is not valid, an empty
      string will be returned
      ||**INPUT VARIABLES**||
      name -> parameter name (as it appears within the extracted configuration);
      supported_values -> a sequence of supported values
      """
      value = str(self.blob['port']['configuration'][name])
      if self.blob['port']['configuration'][name] not in supported_values :
         value = ''
      elif name == 'parity' :
         value = self.translate_parity_type(value)
      return value

   def retrieve(self) :
      stream = open(self.file_path,
                    mode='r')
      self.blob = yaml.safe_load(stream)

   def parse(self) :
      """
      ||**INSTANCE ATTRIBUTE**||
      configuration -> a dictionnary that stores the following keys:
                       - name -> name of the serial port;
                       - baud-rate -> communication speed;
                       - data-bits -> number of data bits that will be recognized in a serial frame;
                       - stop-bits -> number of stop bits that will be recognized in a serial frame;
                       - parity -> parity scheme that will be employed during data exchanges;
                       the default baud rate is 9600, while the default framing is 8N1;
      ||**ERROR CONDITION**||
      if an error condition arises during the parsing operation, the instance attribute will be an empty
      dictionary;
      """
      self.configuration = {}
      if 'port' not in self.blob :
         if self.aLogger :
            self.aLogger.store_message('the configuration root, port, is not defined within the extracted blob',
                                       prefix='[ERR]',
                                       f_ts=True)
      else :
         if 'name' not in self.blob['port'] :
            if self.aLogger :
               self.aLogger.store_message('the serial port name is not defined within the extracted blob',
                                          prefix='[ERR]',
                                          f_ts=True)
         else :
            if 'configuration' not in self.blob['port'] :
               if self.aLogger :
                  self.aLogger.store_message('the serial port configuration is not defined within the extracted blob',
                                             prefix='[ERR]',
                                             f_ts=True)
            else :
               self.configuration['port-name'] = self.blob['port']['name']
               parameter_name = 'baud-rate'
               if parameter_name in self.blob['port']['configuration'] :
                  self.configuration[parameter_name] = self.chk_numerical_parameter(parameter_name,
                                                                                    baud_rates)
               else :
                  self.configuration[parameter_name] = Serial_configurator.default[parameter_name]
               parameter_name = 'data-bits'
               if parameter_name in self.blob['port']['configuration'] :
                  self.configuration[parameter_name] = self.chk_numerical_parameter(parameter_name,
                                                                                    data_bits)
               else :
                  self.configuration[parameter_name] = Serial_configurator.default[parameter_name]
               parameter_name = 'stop-bits'
               if parameter_name in self.blob['port']['configuration'] :
                  self.configuration[parameter_name] = self.chk_numerical_parameter(parameter_name,
                                                                                    stop_bits)
               else :
                  self.configuration[parameter_name] = Serial_configurator.default[parameter_name]
               parameter_name = 'parity'
               if parameter_name in self.blob['port']['configuration'] :
                  self.configuration[parameter_name] = self.chk_string_parameter(parameter_name,
                                                                                 parity_types)
               else :
                  self.configuration[parameter_name] = Serial_configurator.default[parameter_name]

   def create_handler(self,
                      inter_octet_timeout) :
      """
      creates an handler for a serial port. If a configuration could not be parsed correctly,
      no handler will be created
      ||**INPUT VARIABLE**||
      inter_octet_timeout -> time-out, expressed in seconds, between the reception of two adjacent octets
      """
      handler = None
      if self.configuration :
         try :
            handler = Serial(self.configuration['port-name'],
                             baudrate=self.configuration['baud-rate'],
                             bytesize=self.configuration['data-bits'],
                             parity=self.configuration['parity'],
                             stopbits=self.configuration['stop-bits'],
                             xonxoff=False,
                             rtscts=False,
                             dsrdtr=False,
                             inter_byte_timeout=inter_octet_timeout)
         except ValueError :
            handler = None
            self.aLogger.store_message('wrong configuration value',
                                       prefix='[ERR]',
                                       f_ts=True)
         except SerialException :
            handler = None
            self.aLogger.store_message('{} may not exist'.format(port_name),
                                       prefix='[ERR]',
                                       f_ts=True)
      return handler

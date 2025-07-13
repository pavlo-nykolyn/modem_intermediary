# Author: Pavlo Nykolyn
# Last modification date: 08/07/2025

"""
Implements the Modem_response class that enables data exchanges between a DTE
and a DCE
"""

from parsing.modem_command import Modem_command

class Modem_response(Modem_command) :
   delimiter_sequence = b'\x0D\x0A' # used as a dalimiter between printable characters
   value_separator = ',' # the comma is used to separate two adjacent values within the response to an AT command

   def __init__(self,
                c_type,
                aLogger) :
      """
      ||**ATTRIBUTES**||
      c_type -> identifier of the command dispatched by the DTE;
      aLogger -> an instance of the Logger class;
      """
      self.c_type = c_type
      self.aLogger = aLogger

   def tokenize(self,
                blob) :
      """
      extracts delimited tokens contained within a blob. The
      latter is assumed to be an encoded byte sequence;
      """
      split_blob = blob.split(sep=Modem_response.delimiter_sequence)
      return [ element for element in split_blob if element ]

   def extract_string(self,
                      value) :
      """
      extracts a sequence of characters from a delimited string
      """
      return value.strip('"').rstrip('"') # the 3GPP 27.007 standard enforces the use of inverted commas as the delimiter of a string type value

   def extract_parameters(self,
                          value) :
      """
      extracts delimited parameters within the input value. The input value may contain components that are strings
      (as defined by the 3GPP TS 27.007 standard). These strings may contain and embedded character that represents
      the component separator. This function correctly treats them as string characters and not as component separators
      """
      parameters = []
      opening_inverted_comma = False # set to True whenever an opening string delimiter has been found
      is_string = False # set to True whenever a string has been completely consumed
      idx = 0
      while idx < len(value) :
         if value[idx] == '"' :
            if not opening_inverted_comma :
               opening_inverted_comma = True
         elif value[idx] == Modem_response.value_separator :
            if idx :
               if opening_inverted_comma :
                  if value[idx - 1] == '"' :
                     opening_inverted_comma = False
                     is_string = True # a string got acquired
               if not opening_inverted_comma :
                  character_sequence = value[:idx]
                  if character_sequence :
                     if is_string :
                        character_sequence = self.extract_string(character_sequence)
                        is_string = False # a string got released
                     if self.aLogger :
                        self.aLogger.store_message('the following parameter has been extracted: {}'.format(character_sequence),
                                                   prefix='[INF]',
                                                   f_ts=True)
                     parameters.append(character_sequence)
                  value = value[idx + 1:]
                  idx = -1 # the next index shall be 0
            else :
               value = value[idx + 1:]
               idx = -1 # the next index shall be 0
         idx += 1
      if value :
         if is_string :
            value = self.extract_string(value[1:])
         if self.aLogger :
            self.aLogger.store_message('the following parameter has been extracted: {}'.format(value),
                                       prefix='[INF]',
                                       f_ts=True)
         # the last parameter does not end with a separator
         parameters.append(value)
      return parameters

   def translate_sm_status(self,
                           status) :
      """
      translates the status of a short message contained within a storage medium within the transmission equipment
      """
      translated_status = ''
      if self.c_type == Modem_command.commands[0] :
         if status == 'REC READ' :
            translated_status = 'read'
         elif status == 'REC UNREAD' :
            translated_status = 'not_read'
         elif status == 'STO UNSENT' :
            translated_status = 'not_dispatched'
         elif status == 'STO SENT' :
            translated_status = 'dispatched'
      return translated_status

   def extract(self,
               response) :
      """
      attempts data extraction from the response;
      ||**RETURN VALUE**||
      returns a dictionary
      """
      structure = {}
      tokens = self.tokenize(response)
      if ((self.c_type == Modem_command.commands[0] or
           self.c_type == Modem_command.commands[1]) and
          len(tokens) == 1) :
         if self.aLogger :
            self.aLogger.store_message('the response {} does not contain the delimiter sequence {}'.format(response,
                                                                                                           Modem_response.delimiter_sequence),
                                       prefix='[ERR]',
                                       f_ts=True)
      if self.c_type == Modem_command.commands[0] :
         try :
            for token in tokens :
               token = token.decode()
               extraction_error = False # the slot may not reference a valid message
               idx = token.find('+CMGR') # the response can be considered validated if idx is higher than or equal to zero
               if idx == -1 :
                  idx = token.find('+CMS ERROR')
                  if idx >= 0 :
                     extraction_error = True
                  else :
                     unsolicited = token.find('+CMTI') # -1 -> the read operation did not catch an unsolicited SMS-DELIVER indication
                     if (unsolicited == -1 and
                         token != 'ERROR') : # some transmission equipments may return ERROR whenever a slot does not contain a message
                        structure['SMS'] = token
               if (idx >= 0 and
                   not extraction_error) :
                  token = token[idx + 6:] # skipping +CMGR:
                  token = token.strip().rstrip() # removing leading and trailing white-space characters
                  parameters = self.extract_parameters(token)
                  num_parameters = len(parameters)
                  structure['SMS-status'] = self.translate_sm_status(self.extract_string(parameters[0]))
                  structure['SMS-sender'] = self.extract_string(parameters[1])
                  if self.aLogger :
                     self.aLogger.store_message('the response contains {} parameters'.format(num_parameters),
                                                prefix='[INF]',
                                                f_ts=True)
                  if (num_parameters == 3 or
                      num_parameters == 10) :
                     structure['Service-center-timestamp'] = self.extract_string(parameters[2])
                  elif (num_parameters == 4 or
                        num_parameters == 11) :
                     structure['Service-center-timestamp'] = self.extract_string(parameters[3])
         except TypeError :
            if self.aLogger :
               self.aLogger.store_message('token {} contains a value represented through an unexpected data type'.format(token),
                                          prefix='[ERR]',
                                          f_ts=True)
            raise
      elif self.c_type == Modem_command.commands[1] :
         if len(tokens) != 1 :
            if self.aLogger :
               self.aLogger.store_message('the amount of expected tokens for the response to a {} command is 1'.format(Modem_command.commands[1]),
                                          prefix='[ERR]',
                                          f_ts=True)
         token = tokens[0]
         try :
            sequence = []
            token = token.decode()
            idx = token.find('+CPMS')
            if idx >= 0 :
               token = token[idx + 6:] # skipping +CPMS;
               token = token.strip().rstrip() # removing leading and trailing white-space characters
               parameters = self.extract_parameters(token)
               num_parameters = len(parameters)
               if num_parameters == 9 :
                  for parameter in parameters :
                     element = parameter
                     if parameter.isdigit() :
                        element = int(parameter)
                     sequence.append(element)
                  structure['data'] = sequence.copy()
               else :
                  if self.aLogger :
                     self.aLogger.store_message('{} parameters are expected within the response to a {} command'.format(num_parameters,
                                                                                                                        Modem_command.commands[1]),
                                                prefix='[ERR]',
                                                f_ts=True)
         except TypeError :
            if self.aLogger :
               self.aLogger.store_message('token {} contains a value represented through an unexpected data type'.format(token),
                                          prefix='[ERR]',
                                          f_ts=True)
            raise
      return structure

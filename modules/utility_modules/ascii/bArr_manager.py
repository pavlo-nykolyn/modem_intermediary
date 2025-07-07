# Author: Pavlo Nykolyn
# Last modification date: 07/07/2025

"""
collects functions that manipulates bytearray instances
"""

str_ctrl = ('<NUL>',
            '<SOH>',
            '<STX>',
            '<ETX>',
            '<EOT>',
            '<ENQ>',
            '<ACK>',
            '<BEL>',
            '<BS>',
            '<HT>',
            '<LF>',
            '<VT>',
            '<FF>',
            '<CR>',
            '<SO>',
            '<SI>',
            '<DLE>',
            '<DC1>',
            '<DC2>',
            '<DC3>',
            '<DC4>',
            '<NAK>',
            '<SYN>',
            '<ETB>',
            '<CAN>',
            '<EM>',
            '<SUB>',
            '<ESC>',
            '<FS>',
            '<GS>',
            '<RS>',
            '<US>',
            '<SP>',
            '<DEL>'
           )

def byte_to_str(byte,
                aLogger) :
   """
   transforms a byte into a string;
   ||**INPUT PARAMETERS**||
   byte -> an 8-bit unsigned integer
   aLogger -> an instance of the Logger class;
   ||**RETURN VALUE**||
   returns a string form of the byte. In particular, if the byte encodes
           a control character, it will be transformed into an identifier
           enclosed between <>;
           any byte that is encoded as an integer belonging to the [128, 255] interval
           will be transformed into the string form of the nul character;
           ** ERROR CONDITION **
           None will be returned
   """   
   string_form = None
   if (byte > 255 and
       aLogger) :
      aLogger.store_message('{} has to belong to the interval [0, 255]'.format(byte),
                            prefix='[ERR]',
                            f_ts=True)
   else :
      if byte <= 32 :
         string_form = str_ctrl[byte]
      elif byte == 127 :
         string_form = str_ctrl[33]
      elif byte >= 128 :
         string_form = str_ctrl[0]
      else :
         octet = bytearray(1)
         octet[0] = byte
         string_form = octet.decode()
   return string_form

def octet_to_str(octet) :
   """
   attempts the transformation of an octet (a bytes instance of a single element);
   ||**INPUT PARAMETER**||
   octet -> the target;
   ||**RETURN VALUE**||
   returns a string form of the octet. In particular, if the byte encodes
           a control character, it will be transformed into an identifier
           enclosed between <>;
           ** ERROR CONDITION **
           None will be returned
   """
   string_form = None
   if len(octet) == 1 :
      value = int(octet.hex(),
                  16)
      if value <= 32 :
         string_form = str_ctrl[value]
      elif value == 127 :
         string_form = str_ctrl[33]
      else :
         byte = bytearray(1)
         byte[0] = value
         string_form = byte.decode()
   return string_form

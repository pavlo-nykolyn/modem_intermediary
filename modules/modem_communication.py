# Author: Pavlo Nykolyn
# Last modification date: 07/07/2025

"""
this module provides the entry-point for all communication
with modems that support AT commands
"""

import argparse
from manipulators.command_manipulator import Command_manipulator
from data_exchange.modem_request import Modem_request
from data_exchange.poll_wrapper import Poll_wrapper
from utility_modules.input.serial_stream.serial_configurator import Serial_configurator
from utility_modules.logging.logger import Logger

anArgParser = argparse.ArgumentParser(description='punto d\'ingresso per la comunicazione con un modem che supporta comandi AT')

argument_list = ({'namespace-ID' : 'configuration_path',
                  'CLI-ID' : None,
                  'help' : 'path del file .yaml che specifica la configurazione di una porta seriale'},
                 {'namespace-ID' : 'behaviour',
                  'CLI-ID' : None,
                  'help' : 'indica la dinamica dell\'interazione con il modem'},
                 {'namespace-ID' : 'command',
                  'CLI-ID' : '--command',
                  'help' : 'comando da inviare al modem'},
                 {'namespace-ID' : 'message_index',
                  'CLI-ID' : '--message-index',
                  'help' : 'indice del messaggio memorizzato nel dispositivo di trasmissione'},
                 {'namespace-ID' : 'read_tout',
                  'CLI-ID' : '--read-timeout',
                  'help' : 'valore del time-out (espresso in millisecondi), entro il quale deve essere ricevuto almeno un byte al fine di considerare la risposta valida'},
                 {'namespace-ID' : 'inByte_tout',
                  'CLI-ID' : '--inter-byte-timeout',
                  'help' : 'intervallo temporale inter-byte (espresso in millisecondi)'}
                )

anArgParser.add_argument(argument_list[0]['namespace-ID'],
                         action='store',
                         help=argument_list[0]['namespace-ID'])
anArgParser.add_argument(argument_list[1]['namespace-ID'],
                         action='store',
                         choices=['read-all-sms','command'],
                         help=argument_list[1]['namespace-ID'])
anArgParser.add_argument(argument_list[2]['CLI-ID'],
                         action='store',
                         nargs='?',
                         default=None,
                         dest=argument_list[2]['namespace-ID'],
                         help=argument_list[2]['namespace-ID'])
anArgParser.add_argument(argument_list[3]['CLI-ID'],
                         action='store',
                         nargs='?',
                         default=None,
                         dest=argument_list[3]['namespace-ID'],
                         help=argument_list[3]['namespace-ID'])
anArgParser.add_argument(argument_list[4]['CLI-ID'],
                         action='store',
                         type=int,
                         nargs='?',
                         default=None,
                         dest=argument_list[4]['namespace-ID'],
                         help=argument_list[4]['namespace-ID'])
anArgParser.add_argument(argument_list[5]['CLI-ID'],
                         action='store',
                         type=int,
                         nargs='?',
                         default=None,
                         dest=argument_list[5]['namespace-ID'],
                         help=argument_list[5]['namespace-ID'])

arg_ns = anArgParser.parse_args()
dict_ns = vars(arg_ns)

aLogger = Logger()

behaviour = dict_ns[argument_list[1]['namespace-ID']]
command = dict_ns[argument_list[2]['namespace-ID']]
if (behaviour == 'command' and
    not command) :
   aLogger.store_message('a single command has not been indicated',
                         prefix='[ERR]',
                         f_ts=True)
else :
   file_path = dict_ns[argument_list[0]['namespace-ID']]
   inter_octet_timeout = dict_ns[argument_list[5]['namespace-ID']]
   if inter_octet_timeout :
      inter_octet_timeout /= 1000 # this value is to be expressed in seconds
   aConfigurator = Serial_configurator(file_path,
                                       aLogger)
   aConfigurator.retrieve()
   aConfigurator.parse()
   handler = aConfigurator.create_handler(inter_octet_timeout)
   if handler :
      serial_poll_instance = Poll_wrapper('read',
                                          dict_ns[argument_list[4]['namespace-ID']],
                                          handler.fileno())
      command = dict_ns[argument_list[2]['namespace-ID']]
      request_manager = Modem_request(handler,
                                      serial_poll_instance,
                                      aLogger)
      aManipulator = Command_manipulator(request_manager,
                                         aLogger)
      behaviour = dict_ns[argument_list[1]['namespace-ID']]
      information_cluster = None
      if behaviour == 'read-all-sms' :
         information_cluster = aManipulator.read_all_sms()
      elif behaviour == 'command' :
         information_cluster = aManipulator.perform_command(command,
                                                            parameter_sequence=dict_ns[argument_list[3]['namespace-ID']])
      print(information_cluster)
      handler.close()

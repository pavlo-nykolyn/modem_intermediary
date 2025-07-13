# Author: Pavlo Nykolyn
# Last modification date: 13/07/2025

"""
Provides a REST API for the modem_communication program
"""

from flask import Flask, request, jsonify
from manipulators.command_manipulator import Command_manipulator
from data_exchange.modem_request import Modem_request
from data_exchange.poll_wrapper import Poll_wrapper
from utility_modules.input.serial_stream.serial_configurator import Serial_configurator
from utility_modules.logging.logger import Logger

aLogger = Logger()

modem_communication_api_errors = ('errore durante l\'apertura della porta seriale',
                                 )
configuration_file_path = '../modules/configuration/serial.yaml'
read_timeout = 2000 # expressed in milliseconds

modem_intermediary = Flask(__name__)

modem_intermediary.json_provider_class.ensure_ascii = True
modem_intermediary.json_provider_class.compact = True

# [GET] /modem/retrieve_all_sms : performs the retrieval of all the SMs saved into the queried medium
@modem_intermediary.route('/modem/retrieve_all_sms', methods=['GET'])
def retrieve_all_sms():
   aConfigurator = Serial_configurator(configuration_file_path,
                                       aLogger)
   aConfigurator.retrieve()
   aConfigurator.parse()
   handler = aConfigurator.create_handler(None) # no inter-octet time-out will be configured
   if handler :
      serial_poll_instance = Poll_wrapper('read',
                                          read_timeout,
                                          handler.fileno())
      request_manager = Modem_request(handler,
                                      serial_poll_instance,
                                      aLogger)
      aManipulator = Command_manipulator(request_manager,
                                         aLogger)
      information_cluster = aManipulator.read_all_sms()
      handler.close()
      return jsonify(information_cluster), 200
   else :
      error_data = {'message' : modem_communication_api_errors[0]}
      return jsonify(error_data), 500



# Author: Pavlo Nykolyn
# Last modification date: 08/07/2025

"""
a simple class that collects data related to the supported
AT commands
"""

class Modem_command :
   # for the love of God, DO NOT change the position of the elements within commands
   commands = ('read-SMS',
               'get-maximum-record-index',
               'disable-new-message-indication',
               'show-text-mode-parameters',
               'inhibit-text-mode-parameters',
               'delete-SMS',
               'delete-all-SMS',
               'disable-echo',
               'enable-echo',
               'attention' # keep this command as the last one 
              )
   # the value of the 'name' key shall be the same as any element of the commands class attribute
   requests = ({'name' : commands[0],
                'decoded' : 'AT+CMGR={}'}, # the index gets updated dynamically
               {'name' : commands[1],
                'decoded' : 'AT+CPMS?'},
               {'name' : commands[2],
                'decoded' : 'AT+CNMI=0,0,0,0,0'},
               {'name' : commands[3],
                'decoded' : 'AT+CSDH=1'},
               {'name' : commands[4],
                'decoded' : 'AT+CSDH=0'},
               {'name' : commands[5],
                'decoded' : 'AT+CMGD={},0'}, # the index gets updated dynamically
               {'name' : commands[6],
                'decoded' : 'AT+CMGD=0,4'},
               {'name' : commands[7],
                'decoded' : 'ATE0'},
               {'name' : commands[8],
                'decoded' : 'ATE1'},
               {'name' : commands[9],
                'decoded' : 'AT'})

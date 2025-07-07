# Author: Pavlo Nykolyn
# Last modification date: 06/07/2025

"""
collects sequences of valid input values for
the parameters of a serial port
"""

baud_rates = (    50,
                  75,
                 110,
                 134,
                 150,
                 200,
                 300,
                 600,
                1200,
                1800,
                2400,
                4800,
                9600,
               14400,
               19200,
               38400,
               57600,
              115200
             )
parity_types = ('none',
                'even',
                'odd',
                'mark',
                'space'
               )
stop_bits = (1,
             2
            )
data_bits = (5,
             6,
             7,
             8
            )

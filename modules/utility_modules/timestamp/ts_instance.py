# Author: Pavlo Nykolyn
# Last modification date: 03/07/2025

"""
used to manipulate time-stamps formatted as strings
"""

from datetime import datetime

def create_instance_scts_naive(str_ts) :
   """
   creates a naive datetime instance from a service center time-stamp.
   The time zone will not be considered;
   the format of the time-stamp is YY/MM/DD,hh:mm:ss(+|-)zz
   """
   dt = datetime.strptime(str_ts[:17],
                          '%y/%m/%d,%H:%M:%S')
   return dt

def create_instance_scts_aware(str_ts) :
   """
   creates an aware datetime instance form a service center time-stamp;
   the format of the time-stamp is YY/MM/DD,hh:mm:ss(+|-)zz
   """
   pass

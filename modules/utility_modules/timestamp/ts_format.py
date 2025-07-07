# Pavlo Nykolyn
# Last modification date: 18/05/2025

""" a simple module that provides functions that
    tranform a given datetime object into a string """

from datetime import datetime

def get_current_year() :
   """
   retrieves the current year as a string having the format YYYY
   """
   current_ts = datetime.now()
   return current_ts.strftime('%Y')

def get_current_ts() :
   """
   retrieves the current time-stamp as a string having the following
   format: DD/MM/YYYY hh:mm:ss
   """
   current_ts = datetime.now()
   return current_ts.strftime('%d/%m/%Y %H:%M:%S')

def get_current_ts_noTime() :
   """
   retrieves the current time-stamp as a string having the following
   format: YYYY_MM_DD
   """
   current_ts = datetime.now()
   return current_ts.strftime('%Y_%m_%d')

def get_given_ts(given_ts) :
   """
   retrieves the given time-stamp as a string having the following
   format: DD/MM/YYYY hh:mm:ss
   """
   return given_ts.strftime('%d/%m/%Y %H:%M:%S')

def get_given_ts_ms(given_ts) :
   """
   retrieves the given time-stamp as a string having the following
   format: YYYY-MM-DD hh:mm:ss.lll (millisecond resolution)
   """
   given_ts_str = given_ts.strftime('%Y-%m-%d %H:%M:%S.%f')
   return given_ts_str[:-3]

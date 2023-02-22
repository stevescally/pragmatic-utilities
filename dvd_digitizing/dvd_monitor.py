#!/usr/bin/env python

''' 
This script accepts a process id to monitor and then will alert
via text message when the job no longer is running. This is not 
to indicate that the dvd ripping was successfully but more so to
alert when the job has finished and to start on the next dvd.
'''

import time
import psutil
import argparse
from twilio.rest import Client


'''
Input
'''

'''
Script arguments from user.
- PID(s)
- Contact number
'''

def u_args():
   parser = argparse.ArgumentParser()
   parser.add_argument('pid', type=int, nargs='+',
                        help="process id's to monitor")
   parser.add_argument('--contact', type=int, nargs=1,
                       default='15555555555',
                       help="10-digit number to contact XXXXXXXXXXX")
   
   return parser.parse_args()


'''
Watch entered PID(s) 
'''

def watch_pid(pids, contact):
   ''' Check that passed PID(s) exist '''
   while len(pids) != 0 :
      for pid in pids:
        try:
           if psutil.Process(pid).status() == "running":
              print ('Pid ' + str(pid) + ' Status : ' + psutil.Process(pid).status() )
        except psutil.NoSuchProcess:
           print ('PID ' + str(pid) + ' not found\nRemoving PID : ' + str(pid))
           pids.remove(pid)
           send_sms(pid, contact)
      time.sleep(10)


'''
w_pid function will call contact onces a PID no longer is found.
w_pid passes the PID and the contact number to send message to.
'''

def send_sms(pid, number):
   # Your Account Sid and Auth Token from twilio.com/console
   account_sid = ''
   auth_token = ''
   client = Client(account_sid, auth_token)

   message = client.messages \
      .create(
         body='The process ' + str(pid) + ' has finished',
         from_='+15555555555',
         to='+' + str(number)
       )

   print(message.sid) 


'''
Main
'''

''' Gather PID(s) and contact number from user. '''
args = u_args()

print ('PIDS : ' + str(args.pid))
print ('Contact Number : ' + str(args.contact))

''' Watch the PID(s) '''

watch_pid(args.pid, args.contact)


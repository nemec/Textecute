#!/usr/bin/python

import sys
import imaplib
import os
import re
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
from command import exe, shutdown, google, memo, translate, wiki, mail

# This script reads the inbox of the given IMAP server,
# checks for mail from the specified email address (in
# this case, a phone SMS number) and executes the command
# sent in the body of the text based on the functions
# imported from the command module.

# Settings are provided in the file settings.conf

# Created by Daniel Nemec, sources attributed when necessary
# For help or questions, email me at djnemec@gmail.com
# Putting a related subject in the email will help me
# reply to you more quickly.

'''''''''''''''''''''
@TODO Doesn't alert on error. Maybe implement
        error return values for commands?
@TODO Error logging
'''''''''''''''''''''

def log(message):
  "@TODO logging"

def send_mail(to, subject, text):
    # Mail function example found at http://kutuma.blogspot.com
    msg = MIMEMultipart()
    SMTP_SERVER=op['SMTP_SERVER']
    SMTP_PORT=op['SMTP_PORT']
    SMTP_USER=op['SMTP_USER']
    SMTP_PASSWORD=op['SMTP_PASSWORD']
    msg['From'] = SMTP_USER+"@"+SMTP_SERVER[SMTP_SERVER.find('.')+1:]
    msg['To'] = to
    msg['Subject'] = subject

    msg.attach(MIMEText(text))
    mailServer = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(SMTP_USER, SMTP_PASSWORD)
    mailServer.sendmail(SMTP_USER, to, msg.as_string())
    # Should be mailServer.quit(), but that crashes...
    mailServer.close()



# Load from the settings file
settingsFile = open("/home/dan/prg/py/Textecute/settings.conf","r")
settings = settingsFile.readlines()
# Initialize empty list of settings
op={'FROM':'',
    'IMAP_SERVER': 'imap.gmail.com',
    'IMAP_PORT':993,
    'IMAP_USER':'', 'IMAP_PASSWORD':'',
    'SMTP_SERVER':'smtp.gmail.com',
    'SMTP_PORT':587
   }
for line in settings:
  if line[0]=='#':
    continue
  ix = line.find('=')
  if ix < 0:
    log("Cannot read settings file.")
    sys.exit()
  op[line[0:ix].strip().upper()]=line[ix+1:].strip()
settingsFile.close()

# Fail if authentication info is not present.
for operator in ('IMAP_USER', 'IMAP_PASSWORD'):
  if op[operator] == '':
    log("Missing necessary credentials to log in.")
    sys.exit()

# Set SMTP authentication to the same as IMAP
# if none has been provided.
if not op.has_key('SMTP_USER'):
  op['SMTP_USER']=op['IMAP_USER']
if not op.has_key('SMTP_PASSWORD'):
  op['SMTP_PASSWORD']=op['IMAP_PASSWORD']

# If anything is provided on the command line, sends that message
# instead of checking the address - basically acts as a quick and
# dirty of sending a message to the provided cell phone (delayed
# messages, for example, with the 'at' system command)
if len(sys.argv) > 1:
    send_mail(op["FROM"], "", str(sys.argv[1:]))
    sys.exit()


# connect to server
server = imaplib.IMAP4_SSL(op['IMAP_SERVER'], op['IMAP_PORT']) # gmail uses SSL on port 993

# login
server.login(op['IMAP_USER'], op['IMAP_PASSWORD'])
server.select()

# list items on server
typ, data = server.search(None, "UNSEEN")
for num in data[0].split():
    typ, data = server.fetch(num, '(BODY[HEADER.FIELDS (FROM)])')
    frm=re.search("[\w.]*@[\w.]*", data[0][1][6:].strip()).group() # Parses the FROM string so that just the email address is used
    if frm == op['FROM']:
        typ, read = server.fetch(num, '(FLAGS)')
        if read[0].find('\\Seen') == -1:
            typ, dat = server.fetch(num, '(BODY[TEXT])')
            body=dat[0][1].strip()
            # This for-loop is a quick hack to ignore
            # extra data that a gmail address puts in the
            # body of an email when sending. There are no
            # guarantees on correct parsing for all
            # mail servers.
            for line in body.split("\n"):
                line=line.strip()
                if len(line) >0 and not line[0] == "-" \
                  and line.find(":") == -1:
                    body=line
                    break
            if body[0]=='@':
                body=body[1:]
            else:
                body=body.lower()
            ix=body.find(' ')
            returned = ''
            if ix == -1:
                if body in locals():
                    returned = locals()[body]()
                else:
                    returned = "Command not found.\nDid you forget to import it?"
            else:
                # Execute function if provided by command.py
                if body[0:ix] in locals():
                    returned = locals()[body[0:ix]](body[ix+1:])
                else:
                    returned = "Command not found.\nDid you forget to import it?"
            if len(returned) > 160:
                returned = returned[0:160]
            print returned
            if returned > 0: # If there's a returned value, send it back
                send_mail(op['FROM'], "", returned)
    server.store(num, '+FLAGS', '\\Seen') # Mark as read so we only process once

server.expunge()
server.logout()


import imaplib
from email.parser import HeaderParser
import re
import getpass
import argparse
import sys

parser = argparse.ArgumentParser(description='Extract gmail metadata into a csv')
parser.add_argument('-p', '--password', help='Your Authentication Credentials, will ask if none specified', dest='password', required=False)
parser.add_argument('-i', '--inbox', help='Your Inbox to parse', required=False)
parser.add_argument('-e', '--email', help='Your email address', required=False)
parser.add_argument('-f', '--file', help='output file for csv data', required=False)
if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()

#password = getpass.getpass()

if (args.password is False):
    print 'no password specified, ask'
    args.password = getpass.getpass()

if (args.inbox is False):
    print "no inbox specificed"


connection = imaplib.IMAP4_SSL('imap.gmail.com')
connection.login(args.email, args.password)

f = open('mail.csv', 'w')

#filter = re.match('Re:')

# Select the mail box
status, messages = connection.select(args.inbox)

filter = "Re: "

if status != "OK":
    print "Incorrect mail box"
    exit()

if int(messages[0]) > 0:


    for message_number in range(1,int(messages[0])+1):
        data = connection.fetch(message_number, '(BODY[HEADER])')
        parser = HeaderParser()
        msg = parser.parsestr(data[1][0][1])
        if msg['to'] == 'security@puppetlabs.com':
		s = msg['subject']
		if s.find(filter) == -1:
			print "To: %s" % msg['to'] + "\t" + "From: %s" % msg['from'].rstrip('\r\n') + "\t" + "Subject: %s" % msg['subject'] + "\t" + "Date: %s" % msg['date']
			f.write("To: %s" % msg['to'] + "\t" + "From: %s" % msg['from'].rstrip('\r\n') + "\t" + "Subject: %s" % msg['subject'] + "\t" + "Date: %s" % msg['date'] + "\n")
	#print "Subject: %s" % msg['subject']
        # print "From: %s" % msg['from']


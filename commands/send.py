#!/usr/bin/python

import requests
import json
from base64 import b64encode
from re import split as re_split
from os import path
from sys import stdin
from markdown import markdown

description = 'A command for sending emails by using the Mandrill API by MailChimp! Created with love by Luis Ferrer-Labarca'

def create_tos(emails, the_type): #Simple method for creating dictionaries acceptable by the Mandrill API in the 'attachments' section
	result = []
	for email in emails:
		to = {'email':email, 'type':the_type}
		result.append(to)
	return result

def split_options(options): #Spliting the options that accept multiple elements (emails, attachments, etc)
	regex = '[ ,]+'
	return [option for option in re_split(regex, options) if option != '']

def run(options, parser, key):

	url = 'https://mandrillapp.com/api/1.0/messages/send.json' #Url for sending emails through MailChimp API

	#Adding all accepted arguments for the command. help is what is shown when you use the -h or --help flag after the command (e.g. mandrill -h)
	parser.add_argument('-md', '--message-md', action='store_true', help='Signals that the message for the email is in Markdown format.')
	parser.add_argument('-m', '--message', default=stdin.read() if not stdin.isatty() else '', help='Message for the email in HTML format (or plain text).')
	parser.add_argument('-s', '--subject', default='', help='Subject for the email.')
	parser.add_argument('from_email', help='Email address that is sending the email.')
	parser.add_argument('-n', '--name', default='', help='Name of the person sending the email.')
	parser.add_argument('to_email', help='Email address(es) where the email is being sent separated by commas/spaces. If spaces then wrap around quote marks.')
	parser.add_argument('-c', '--cc', default='', help='Email address(es) to send the email as CC. If spaces then wrap around quote marks.')
	parser.add_argument('-I', '--important', action='store_true', help='Marks email as important.')
	parser.add_argument('-a', '--attachment', default='', help='Adds attachment(s) separated by commas/spaces. If spaces then wrap around quote marks.')

	options = parser.parse_args(args=options) #Parsing arguments from the options passed. Creates an object

	#Extracting info from the Parser
	message = markdown(options.message) if options.message_md else options.message
	subject = options.subject
	from_email = options.from_email
	from_name = options.name if options.name else from_email
	important = options.important
	attachments = split_options(options.attachment) #Using split_options so I get filter empty strings in the list
	to_emails = split_options(options.to_email)
	ccs = split_options(options.cc)

	#Dictionary to be converted to JSON before sending the request
	request = {
	    'key': key,
	    'message': {
		'html': message,
		'text': 'Example text content',
		'subject': subject,
		'from_email': from_email,
		'from_name': from_name,
		'to': [],
		'attachments': [],
		'headers': {
		    'Reply-To': from_email
		},
		'important': important,
		'merge': True,
		'merge_language': 'mailchimp'
	    },
	}

	#Adding the emails to the request
	emails = create_tos(to_emails, 'to')
	request['message']['to'] += emails

	#Adding CCs to the request if any
	if ccs != []:
		emails = create_tos(ccs, 'cc')
		request['message']['to'] += emails

	#Adding attachments to the request if any
	if attachments != []:
		for attachment in attachments:
			attachment_file = open(path.expanduser(attachment))
			attachment_text = attachment_file.read().strip()
			attachment_file.close()		

			request['message']['attachments'] += [
				{

					'type': 'text/plain',
					'name': attachment,
					'content': b64encode(attachment_text)
				}
			]

	#Sending request and printing response!
	r = requests.post(url, json=request)
	return r.text

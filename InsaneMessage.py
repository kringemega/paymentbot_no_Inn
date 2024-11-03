import os
from getpass import getuser
from sys import argv
from datetime import datetime
import shutil

def get_num_read():
	with open('/var/local/messager/' + getuser() + '/read', 'r') as f:
		return int(f.read())

def get_num_msgs():
	with open('/var/local/messager/' + getuser() + '.num', 'r') as f:
		return int(f.read())

def get_file_names():
	files = os.listdir('/var/local/messager/' + getuser())
	files.remove('read')
	if files == []:
		return []
	ret = []
	nums = []
	for f in files:
		nums.append(int(f.split('_')[0]))
	for i in range(max(nums)):
		ret.append(files[nums.index(min(nums))])
		files.pop(nums.index(min(nums)))
		nums.pop(nums.index(min(nums)))
	return ret

def check():
	"""Returns the number of unread messages"""
	num_read = get_num_read()
	num_msgs = get_num_msgs()
	return num_msgs - num_read

def check_string():
	"""Prints the string used on login."""
	num = check()
	if num == 0:
		print('You have no unread messages.')
	else:
		print('You have ' + str(num) + ' unread messages. Use `messager read` to read them.')

def msg_list(n=None):
	files = get_file_names()
	print('{:>5}{:>20}{:>15}'.format('#', 'From', 'Date'))
	if n != None:
		if n < len(files):
			files = files[len(files) - n:]
	for f in files:
		temp = f.split('_')
		print('{:>5}{:>20}{:>15}'.format(temp[0], temp[1], temp[2][0:10]))

def read_spf_msg(n):
	for f in get_file_names():
		temp = f.split('_')
		if int(temp[0]) == n:
			print('From: ' + temp[1] + ', Date: ' + temp[2])
			with open('/var/local/messager/' + getuser() + '/' + f, 'r') as msg:
				print(msg.read())
			return
	print('Message not found.')

def read_msgs():
	"""Shows unread messages in a menu-like way"""
	num_read = get_num_read()
	num_msgs = get_num_msgs()
	files = get_file_names()
	if files == []:
		print('You have no messages to read.')
		return
	user = getuser()
	prefix = '/var/local/messager/' + user + '/'
	count = 0
	for f in files:
		temp = f.split('_')
		if int(temp[0]) > num_read + count:
			count += 1
			print('From: ' + temp[1] + ', Date: ' + temp[2])
			with open(prefix + f, 'r') as curr_file:
				print(curr_file.read())
			with open('/var/local/messager/' + user + '/read', 'w+') as read_file:
				read_file.write(str(num_read + count))
		if num_read + count < num_msgs:
			print('Would you like to read the next message? (y/n)')
			ans = input()
			while(ans not in 'ynYN'):
				print('Unknown response. Would you like to keep reading them? (y/n)')
				ans = input()
			if ans in 'nN':
				return
		else:
			print('You\'re all caught up!')
			return
	print('You\'re all caught up!')

def get_date():
	return datetime.now().strftime('%Y-%m-%d-%H:%M')

def make_name(user):
	"""Creates a file name based on the specified user's messages."""
	return str(get_num_msgs() + 1) + '_' + getuser() + '_' + get_date()

def send_msg(user=None):
	"""Puts the user through a menu, asking for user then message contents.
	Sends the mail after."""
	users = os.listdir('/var/local/messager/')
	while user not in users:
		if user != None:
			print('User not found. Try again.')
		print('Who would you like to send the mail to? Enter username.')
		user = input()
	print('Enter message text:')
	text = input()
	full_text = ''
	while text != '':
		full_text += text
		text = input()
	file_name = '/var/local/messager/' + user + '/' + make_name(user)
	with open(file_name, 'w') as msg_file:
		msg_file.write(full_text)
	num_msgs = get_num_msgs()
	with open('/var/local/messager/' + user + '.num', 'w') as num_file:
		num_file.write(str(num_msgs + 1))
	shutil.chown(file_name, user=user, group=user)

def get_help():
	print('messager is a python-based messaging application for use with linux servers, written and maintained by derekthesnake.')
	print('All options can be replaced with the first letter of the option, with or without a dash.')
	print('Options:\n')
	print('check:')
	print('\t`messager check` is usually put into ~/.bashrc, it checks if the user has any unread messages.')
	print('help:')
	print('\t`messager help` prints this menu.')
	print('list:')
	print('\t`messager list` lists the user\'s recieved messages.')
	print('\t`messager list <number>` lists the user\'s last <number> of received messages.')
	print('read:')
	print('\t`messager read` allows the user to iterate through their unread messages.')
	print('\t`messager read <message number>` allows the user to read a specific message.')
	print('send:')
	print('\t`messager send` allows the user to send mail to another user, prompted by the program.')
	print('\t`messager send <username>` sends mail to the specified user.')

def invalid_option():
	print('Invalid option. Try `messager help` to see available options.')

if len(argv) == 1:
	print('Try `messager help` to see available options.')
elif argv[1] == '-':
	invalid_option()
elif argv[1] == 'read' or argv[1] in '-r':
	if len(argv) == 2:
		read_msgs()
	else:
		read_spf_msg(int(argv[2]))
elif argv[1] == 'check' or argv[1] in '-c':
	check_string()
elif argv[1] == 'send' or argv[1] in '-s':
	try:
		send_msg(user=argv[2])
	except IndexError:
		send_msg()
elif argv[1] == 'list' or argv[1] in '-l':
	if argv[2] != None:
		msg_list(int(argv[2]))
	else:
		msg_list()
elif argv[1] == 'help' or argv[1] in '-h':
	get_help()
else:
	invalid_option()
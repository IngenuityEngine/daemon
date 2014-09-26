import os
import sys
import time
import ctypes

import ieInit
ieInit.init()
import ieGlobals

errCount = 0

def init():
	global errCount
	errCount = 0

def getCommands():
	try:
		f = open('../test/commands.txt')
		commands = filter(None, (line.rstrip() for line in f))
		f.close()
		return commands
	except:
		print >> sys.stderr, 'Error reading from file.'

def getCommandInfo(command):
	cmd = ' '.join(command.strip().split()[1:])
	compTypes = command.split()[0]
	compTypes = compTypes.split(',')
	return compTypes, cmd, command

def update():
	commands = getCommands()
	commands = [getCommandInfo(c) for c in commands]
	for compTypes, cmd, command in commands:
		if ieGlobals.COMPUTER_TYPE in compTypes:
			try:
				print 'Executing %s.' % cmd
				err = os.system(cmd)
				if (not err):
					clear(command)
				else:
					error(cmd, err)
			except:
				error(cmd, ctypes.get_errno())
		else:
			clear(command)

def clear(command):
	f=open('../test/commands.txt')
	lines = f.readlines()
	f.close()
	f = open('../test/commands.txt', 'w')
	for line in lines:
		if (line.strip() and normalizeLine(line) != normalizeLine(command)):
			f.write(line)
	f.close()

def normalizeLine(line):
	if (line[-1] == '\n'):
		return line[:-1]
	return line

def error(cmd, errno):
	global errCount
	errCount += 1
	print >> sys.stderr, 'Error on %s.  Error number %d.  Number of errors is: %d.' % (cmd, errno, errCount)

def runDaemon():
	init()
	while (1):
		update()
		time.sleep(15)

if __name__ == '__main__':
	runDaemon()



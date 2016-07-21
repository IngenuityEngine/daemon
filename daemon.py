# Daemon Simple daemon that listens for and runs commands

# Modules
# import os
# import sys
import time

# Our modules
import arkInit
arkInit.init()
import settingsManager
globalSettings = settingsManager.globalSettings()
from database import Database
import cOS

# Global vars
database = Database()
errCount = 0

# Function: init()
# Set up daemon
def init():
	# Connect to Caretaker Database
	database.connect()

# Function: getCommands()
# Reads commmand info dicts from Caretaker
# stripping whitespace characters from beginning and end of string
# Inputs: none
# Outputs: filtered comands
def getCommands():
	commandDicts = database.find('command').execute()
	return commandDicts

# Function: getCommandInfo(command)
# Parses command info from a string
# Inputs: command (string)
# Outputs: a tuple - a parsed command as a comma-deliniated list,
#					raw command,
#					and original command dict
def getCommandInfo(commandDict):
	# Parse command
	rawCommand = commandDict['command']
	# remove whitespace and parse into command list
	rawCommand.strip()
	commandList = rawCommand.split()
	# Save original raw command (now w/o extra whitespace)
	rawCommand = ' '.join(commandList)
	return commandList, rawCommand, commandDict

# Function: update()
# Gets commands and parses command info for all commands in file
# Executes all valid commands and clears from commands file
# Inputs: none
# Outputs: none, prints executed commands to console
def update():
	print '****UPDATE****'
	rawCommands = getCommands()
	# If no commands, pass
	if not rawCommands:
		return

	commands = [getCommandInfo(c) for c in rawCommands]
	print '****Commands****'
	for command in commands:
		print 'command %s with list %s and raw command %s' % (command[2]['name'], command[0], command[1])
	print 'computer is type ' + globalSettings.COMPUTER_TYPE
	# possible comptuer types are 'workstation' or 'render'
	# TODO: add develop type

	for commandList, rawCommand, commandDict in commands:
		name = commandDict['name']
		data = None
		if 'data' in commandDict:
			data = commandDict['data']
		compTypes = commandDict['type']

		if globalSettings.COMPUTER_TYPE in compTypes:
			# getCommandOutput returns (STDOUT, STDERR)
			out, err = cOS.getCommandOutput(commandList)
			if err:
				print '\nerror:\n', err
			else:
				print '\nout: \n', out
				print '\nBackup %s complete.\n' % database
		else:
			print 'Command %s not applicable for this computer type %s, passing...' % (name, globalSettings.COMPUTER_TYPE)
			continue
			# TODO: don't actually clear it
			# essentially just pretend to execute. timestamp will deal with it anyway

# 	for compTypes, cmd, command in commands:
# 		if globalSettings.COMPUTER_TYPE in compTypes:
# 			try:
# 				print 'Executing %s.' % cmd
# 				err = os.system(cmd)
# 				if (not err):
# 					clear(command)
# 				else:
# 					error(cmd, err)
# 			except:
# 				error(cmd, ctypes.get_errno())
# 		else:
# 			clear(command)

# # Function: clear(command)
# # Rewrites completed or inapplicable commands to commands.txt file
# # Inputs: command, called from update()
# # Outputs: none, writes to commands.txt
# def clear(command):
# 	f=open('../test/commands.txt')
# 	lines = f.readlines()
# 	f.close()
# 	f = open('../test/commands.txt', 'w')
# 	for line in lines:
# 		if (line.strip() and normalizeLine(line) != normalizeLine(command)):
# 			f.write(line)
# 	f.close()

# # Function: normalizeLine(line)
# # Helper function to remove newlines, if they exist
# # Inputs: line to normalize
# # Outputs: normalized line
# def normalizeLine(line):
# 	if (line[-1] == '\n'):
# 		return line[:-1]
# 	return line

# # Function: error(cmd, errno)
# # Maintains the global errCount, incrementing
# # and printing passed error to console
# # Inputs: cmd, command to process, and errno, received error
# # Outputs: none, prints error process, number, and total error count to console
# def error(cmd, errno):
# 	global errCount
# 	errCount += 1
# 	print >> sys.stderr, 'Error on %s.  Error number %d.  Number of errors is: %d.' % (cmd, errno, errCount)

# Function: runDaemon()
# Initializes and loops the daemon's update function, every 15 ms
# Inputs: none
# Outputs: none
def runDaemon():
	init()
	while (1):
		update()
		time.sleep(15)

# Main
if __name__ == '__main__':
	runDaemon()

# OLD
##################################################################################

# # Daemon Simple daemon that listens for and runs commands

# # Modules
# import os
# import sys
# import time
# import ctypes

# # Our modules (TODO: does ieInit exist?)
# import arkInit
# arkInit.init()
# import settingsManager
# globalSettings = settingsManager.globalSettings()

# # Global vars
# errCount = 0

# # Function: init()
# # Set up daemon
# def init():
# 	global errCount
# 	errCount = 0

# # Function: getCommands()
# # Reads commands from commands.txt,
# # stripping whitespace characters from beginning and end of string
# # Inputs: none
# # Outputs: filtered comands
# def getCommands():
# 	try:
# 		f = open('../test/commands.txt')
# 		commands = filter(None, (line.rstrip() for line in f))
# 		f.close()
# 		return commands
# 	except:
# 		print >> sys.stderr, 'Error reading from file.'

# # Function: getCommandInfo(command)
# # Parses command info from a string
# # Inputs: command
# # Outputs: a tuple, of comma-delimited datatypes, parsed command, and original command
# def getCommandInfo(command):
# 	cmd = ' '.join(command.strip().split()[1:])
# 	compTypes = command.split()[0]
# 	compTypes = compTypes.split(',')
# 	return compTypes, cmd, command

# # Function: update()
# # Gets commands and parses command info for all commands in file
# # Executes all valid commands and clears from commands file
# # Inputs: none
# # Outputs: none, prints executed commands to console
# def update():
# 	commands = getCommands()
# 	commands = [getCommandInfo(c) for c in commands]
# 	for compTypes, cmd, command in commands:
# 		if globalSettings.COMPUTER_TYPE in compTypes:
# 			try:
# 				print 'Executing %s.' % cmd
# 				err = os.system(cmd)
# 				if (not err):
# 					clear(command)
# 				else:
# 					error(cmd, err)
# 			except:
# 				error(cmd, ctypes.get_errno())
# 		else:
# 			clear(command)

# # Function: clear(command)
# # Rewrites completed or inapplicable commands to commands.txt file
# # Inputs: command, called from update()
# # Outputs: none, writes to commands.txt
# def clear(command):
# 	f=open('../test/commands.txt')
# 	lines = f.readlines()
# 	f.close()
# 	f = open('../test/commands.txt', 'w')
# 	for line in lines:
# 		if (line.strip() and normalizeLine(line) != normalizeLine(command)):
# 			f.write(line)
# 	f.close()

# # Function: normalizeLine(line)
# # Helper function to remove newlines, if they exist
# # Inputs: line to normalize
# # Outputs: normalized line
# def normalizeLine(line):
# 	if (line[-1] == '\n'):
# 		return line[:-1]
# 	return line

# # Function: error(cmd, errno)
# # Maintains the global errCount, incrementing
# # and printing passed error to console
# # Inputs: cmd, command to process, and errno, received error
# # Outputs: none, prints error process, number, and total error count to console
# def error(cmd, errno):
# 	global errCount
# 	errCount += 1
# 	print >> sys.stderr, 'Error on %s.  Error number %d.  Number of errors is: %d.' % (cmd, errno, errCount)

# # Function: runDaemon()
# # Initializes and loops the daemon's update function, every 15 ms
# # Inputs: none
# # Outputs: none
# def runDaemon():
# 	init()
# 	while (1):
# 		update()
# 		time.sleep(15)

# # Main
# if __name__ == '__main__':
# 	runDaemon()
#



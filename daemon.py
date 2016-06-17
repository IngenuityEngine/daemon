# Daemon Simple daemon that listens for and runs commands

# Modules
import os
import sys
import time
import ctypes

# Our modules (TODO: does ieInit even point to anything?)
# import ieInit
# ieInit.init()
import settingsManager
globalSettings = settingsManager.globalSettings()

# Global vars
errCount = 0

# Function: init()
# Set up daemon
def init():
	global errCount
	errCount = 0

# Function: getCommands()
# Reads commands from commands.txt,
# stripping whitespace characters from beginning and end of string
# Inputs: none
# Outputs: filtered comands
def getCommands():
	try:
		f = open('../test/commands.txt')
		commands = filter(None, (line.rstrip() for line in f))
		f.close()
		return commands
	except:
		print >> sys.stderr, 'Error reading from file.'

# Function: getCommandInfo(command)
# Parses command info from a string
# Inputs: command
# Outputs: a tuple, of comma-delimited datatypes, parsed command, and original command
def getCommandInfo(command):
	cmd = ' '.join(command.strip().split()[1:])
	compTypes = command.split()[0]
	compTypes = compTypes.split(',')
	return compTypes, cmd, command

# Function: update()
# Gets commands and parses command info for all commands in file
# Executes all valid commands and clears from commands file
# Inputs: none
# Outputs: none, prints executed commands to console
def update():
	commands = getCommands()
	commands = [getCommandInfo(c) for c in commands]
	for compTypes, cmd, command in commands:
		if globalSettings.COMPUTER_TYPE in compTypes:
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

# Function: clear(command)
# Rewrites completed or inapplicable commands to commands.txt file
# Inputs: command, called from update()
# Outputs: none, writes to commands.txt
def clear(command):
	f=open('../test/commands.txt')
	lines = f.readlines()
	f.close()
	f = open('../test/commands.txt', 'w')
	for line in lines:
		if (line.strip() and normalizeLine(line) != normalizeLine(command)):
			f.write(line)
	f.close()

# Function: normalizeLine(line)
# Helper function to remove newlines, if they exist
# Inputs: line to normalize
# Outputs: normalized line
def normalizeLine(line):
	if (line[-1] == '\n'):
		return line[:-1]
	return line

# Function: error(cmd, errno)
# Maintains the global errCount, incrementing
# and printing passed error to console
# Inputs: cmd, command to process, and errno, received error
# Outputs: none, prints error process, number, and total error count to console
def error(cmd, errno):
	global errCount
	errCount += 1
	print >> sys.stderr, 'Error on %s.  Error number %d.  Number of errors is: %d.' % (cmd, errno, errCount)

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



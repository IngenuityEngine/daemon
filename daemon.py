# Daemon Simple daemon that listens for and runs commands
# For cross-platform compatability, python commands recommended but not required
# possible computer types are 'workstation', 'render', 'develop'
# multiple computer types permitted per command

# Modules
import sys
import time

# Our modules
import arkInit
arkInit.init()
import settingsManager
globalSettings = settingsManager.globalSettings()
from database import Database
import cOS
import arkUtil
currentComputerSettings = settingsManager.databaseSettings(
	'daemon',
	globalSettings.UNIQUE_NAME)

# Global vars
database = Database()
python = globalSettings.ARK_PYTHON

# Function: init()
# Set up daemon
def init():
	# Connect to Caretaker Database
	database.connect()

	# Set lastRun and failedJobs to defaults - epoch and empty list
	currentComputerSettings.set('lastRun', 0).save()
	currentComputerSettings.set('failedJobs', []).save()

# Function: getCommands()
# Reads commmand info dicts from Caretaker
# Inputs: none
# Outputs: commands
def getCommands():
	lastRun = currentComputerSettings.get('lastRun')
	# if lastRun is none, first time daemon being run, set to epoch
	if not lastRun:
		lastRun = 0
		currentComputerSettings.set('lastRun', lastRun).save()
	commandDicts = database.find('command') \
							.sort('priority', 'desc') \
							.where('enabled', 'is', True) \
							.where('updated', 'greater than', lastRun) \
							.execute()
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
	# If path a command in list, ensure normalized
	for item in commandList:
		item = cOS.normalizePath(item)
	# Save original raw command (now w/o extra whitespace)
	rawCommand = ' '.join(commandList)
	return commandList, rawCommand, commandDict

# Function: update()
# Gets commands and parses command info for all commands in file
# Executes all valid commands and handles any errors
# Sets lastRun to current timestamp
# Inputs: none
# Outputs: none, prints executed commands to console
def update():
	print '\n================UPDATING================='
	rawCommands = getCommands()
	# If no commands, pass
	if not rawCommands:
		print '\nNo new commands to evaluate. Passing...'
		return

	print '\nDaemon running on computer \'%s\' of type \'%s\'' % (globalSettings.COMPUTER_NAME, globalSettings.COMPUTER_TYPE)

	commands = [getCommandInfo(c) for c in rawCommands]

	for commandList, rawCommand, commandDict in commands:
		name = commandDict['name']
		print '\nEvaluating command \'%s\' with raw command:\n\"%s\"' % (name, rawCommand)
		compTypes = commandDict['type']

		# possible computer types are 'workstation', 'render', 'developer'
		if globalSettings.COMPUTER_TYPE in compTypes:
			process = cOS.startSubprocess(commandList, shell=True)
			out, err = cOS.waitOnProcess(process)
		# if computer not in types, pass. timestamp will consider this executed
		else:
			print '\nCommand \'%s\' not applicable for this computer type %s, passing...' % (name, globalSettings.COMPUTER_TYPE)
			continue
	# Record time as last run
	currentComputerSettings.set('lastRun', currentMilliTime()).save()
	# TODO: use database time instead of local time
	# currentComputerSettings.set('lastRun', database.getTime()).save()

# Function: error(cmdInfo, err)
# Prints err
# Inputs: cmdInfo, command to process, and err, received error
# Outputs: none, prints error information to console, adds failed command to failedCommands list
def error(cmdInfo, err):
	# print error
	name = cmdInfo['name']
	print >> sys.stderr, '\nError on \'%s\':\n%s' % (name, err)

	# Add failed job to list of failed jobs
	failedJobs = currentComputerSettings.get('failedJobs')
	failedJobs = arkUtil.ensureArray(failedJobs)

	# if name not in failedJobs:
	if name not in failedJobs:
		print '\nAdding failed job \'%s\' to failedJobs list' % name
		failedJobs.append(name)
	currentComputerSettings.set('failedJobs', failedJobs).save()

# Function: runFailed()
# Gets and runs all failed jobs
# Inputs: none
# Outputs: none, prints information to console
def runFailed():
	print '\n=============RETRYING FAILED============='
	failedJobs = currentComputerSettings.get('failedJobs')
	# If no commands, pass
	if not failedJobs:
		print '\nNo failed jobs to retry. Passing...'
		return

	print '\nRetrying failed jobs %s' % failedJobs
	for job in failedJobs:
		command = database.findOne('command').where('name', 'is', job).execute()
		if not command:
			print 'Failed job no longer exists, passing...'
			continue
		commandList, rawCommand, commandDict = getCommandInfo(command)

		name = commandDict['name']
		print '\nEvaluating failed command \'%s\' with raw command:\n\"%s\"' % (name, rawCommand)

		# If added to failed jobs, already applicable to this computer
		out, err = cOS.getCommandOutput(commandList)
		if err:
			error(commandDict, err)
		else:
			print out

# currentMilliTime()
# Helper to get current timestamp in millisecond format
# Returns 13 digit timestamp, compatible with database's updated timestamps
def currentMilliTime():
	return int(round(time.time()*1000))

# Function: runDaemon()
# Initializes and loops the daemon's update function, every 15 ms
# Inputs: none
# Outputs: none
def runDaemon():
	init()
	count = 0
	while (1):
		update()
		count += 1
		if count > 4: # once time.sleep changed to 60, change this to 10
			runFailed()
			count = 0
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



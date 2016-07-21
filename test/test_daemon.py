
# Standard modules
from expects import *
import time

# Our modules
import arkInit
arkInit.init()

import tryout
from translators import Events
from database import Database
database = Database()
database.connect()

class test(tryout.TestSuite):

	def setUpClass(self):
		self.database = Database()
		self.database.connect()

	def setUp(self):
		print self.database.remove('command').multiple().execute()
		print self.database.create(
			'command',
			{
				'name': 'test',
				'command': 'echo \'hi\'',
				'type': ['developer','workstation'],
			}).execute()

		print self.database.create(
			'command',
			{
				'name': 'echo hello',
				'command': 'echo \'hello\'',
				'type': ['developer'],
				'priority': 40,
				'enabled': True,
			}).execute()

		print self.database.create(
			'command',
			{
				'name': 'echo yo',
				'command': 'echo \'yo\'',
				'type': ['developer'],
				'enabled': False,
			}).execute()

		print self.database.create(
			'command',
			{
				'name': 'ls',
				'command': 'ls .',
				'type': ['developer', 'workstation', 'render'],
			}).execute()

		print self.database.create(
			'command',
			{
				'name': 'python says hi',
				'command': 'python C:/ie/daemon/test/scripts/testCommand.py',
				'type': 'developer',
			}).execute()

		print self.database.create(
			'command',
			{
				'name': 'fake',
				'command': 'fake fake fake this will fail',
				'type': 'developer',
			}).execute()

		print self.database.create(
			'command',
			{
				'name': 'also fake',
				'command': 'also fail because super fake',
				'type': ['developer', 'render'],
			}).execute()

	def findCommands(self):
		commands = self.database.find('command').execute()
	# 	commands = database.find('command')\
	# 		.sort('priority','desc')
	# 		.where('enabled','is',True)
	# 		.where('updated','greater than', lastRun)
	# 		.execute()

		# self.assertEqual(len(commands), 5)
		self.assertTrue(len(commands))

		# test cases:
		# adding commands normally to the database (shoudl be able to find the right number of commands)
		# call getCommands for those and see how many it returns
		# get command info should parse commands with weird whitespace and return correctly
		# call update, it should not run if commands are older than last run

if __name__ == '__main__':
	tryout.run(test)

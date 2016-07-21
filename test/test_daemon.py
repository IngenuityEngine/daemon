
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
				'data': {'some':'data'},
				'type': 'rendernodes',
			}).execute()

		print self.database.create(
			'command',
			{
				'name': 'echo',
				'command': 'echo \'hello\'',
				'data': {'some':'data'},
				'type': 'rendernodes',
			}).execute()

	def findCommands(self):
		commands = self.database.find('command').execute()
	# 	commands = database.find('command')\
	# 		.sort('priority','desc')
	# 		.where('enabled','is',True)
	# 		.where('updated','greater than', lastRun)
	# 		.execute()

		self.assertEqual(len(commands), 2)

if __name__ == '__main__':
	tryout.run(test)

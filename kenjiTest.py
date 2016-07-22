import arkInit
arkInit.init()

from database import Database
import settingsManager
globalSettings = settingsManager.globalSettings()

# comment

database = Database()
database = database.connect()

		# .where('status','in',['queued', 'rendering'])\
		# .where('errors','in',[None, 0,1,2,3,4,5])\
		# .where('errors','less than', 10)\
		# .where('errors','notexists')\
		# .sort('priority','desc')\
# results = database.remove('shepherdJob')\
# 		.where('status','is','complete')\
# 		.multiple(True)\
# 		.options('undo', False)\
# 		.execute()


		# .multiple(True)\
		# .options('undo', False)\
		# .where('name','contains','pvh')\
results = database.find('shepherdJob')\
		.where('name','contains','h264')\
		.execute()

print 'Result:', results
print 'Job count:', len(results)

for x in results:
	if 'pvh' in x['name'].lower():
		print x['name']
		database.update('shepherdJob')\
			.where('_id','is',x['_id'])\
			.set('status','queued')\
			.execute()
	# try:
	# 	print x['priority']
	# except:
	# 	print x['name']

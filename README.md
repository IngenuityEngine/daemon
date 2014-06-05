daemon
======

Simple daemon that listens for and runs commands



Example commands:

pip uninstall GitPython -y
pip install GitPython==0.3.2.RC1


python c:\ie\ark\Install\setup.py -quiet

cp "C:\ie\ark\bin\HardUpdate.lnk" "C:\Users\%USERNAME%\Desktop\HardUpdate.lnk"



# Daemon Command System

Handles command queue for Sheep

Implementation
- problem is backlog of commands when systems become unsync'd
	- only ever maybe 20 commands as they're overwritten (script-enforced unique names)
	- new node comes online, sheep has no script date
	- gets all scripts cuz no script date
	- runs each script
	- only after running all scripts is script date updated
	- if it fails while running a script and crashes out it will start over from the top
		- pretty edgy and not the end of the world, scripts should all run
		- scripts should have a fails number that gets incremented
- want commands that are always run
- want conditionals on commands
	- commands are python scripts, python scripts handle conditionals
- want to be able to run commands in sequence
	- commands have priority, run highest to lowest
- need to be able to run commands on both windows, mac, and linux
	- commands are always python scripts, python handles platform specific execution
- need a way to issue common commands
	- ex: restart sheep, update git
	- just "refresh" existing commands
- want only one restart command or one update command to be active
	- commands should overwrite commands of the same name
	- ex: "restart sheep" clears out other "restart sheep" commands before adding
- want frequent command list
	- commands can be "refreshed"
	- hack: disable / enable them to change updated date
- want command status
	- special field: command status
		- get all sheep
		- get get script date
		- count ones that haven't run yet, display as %
- example add command
	- name:
		restart sheep
	- command:
		python code or script
		ex: shepherd/restartSheep.py
		paths are relative to tools root
	- enabled
	- priority:
		order in which commands will be run, highest first

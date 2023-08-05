# ghettorecorder Package
import json import configparser import requests

	
	Runs on Python 3.5:  R E A D --> (Windows 'pip'/Linux 'pip3, python3') 
	'pip install ghettorecorder' - with a normal user account
		then 
	'pip show ghettorecorder' to find the install Location: site-packages/ghettorecorder / 
	
	-> 'python - m ghettorecorder.run' will run the recorder from anywhere.
	GhettoRecorder is uninstalled by 'pip uninstall gettorecorder'. Recorded mp3 files not.
	
	The 'run.py' is the script, 'settings.ini' has your radio stations and urls.
	Copy 'run.py' and 'settings.ini' files wherever you want to have your record repository.
	
	Magic number 42 is used to connect to all radios found in 'settings.ini'. This is the ^^data base^^.
	
Windows
	"python -m ghettorecorder.run" 
		'pip show ghettorecorder' 
			for install location: site-packages/ghettorecorder
				and recorded files
					'python - m ghettorecorder.run'
Linux
	"python3 -m gettorecorder.run" ('python' IS version 2 and will NOT start)
		'pip3 show ghettorecorder' 
			for install location: site-packages/ghettorecorder
					and recorded files
						'python3 - m ghettorecorder.run'
					
	
	"Records internet radio in files. Mostly 'Artist - title.mp3' style.
	

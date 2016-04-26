#!/usr/bin/python

# python-sql-backup
# Author: Alessio Occhipinti / @lasalefamine / https://github.com/LasaleFamine
# Description: Script to make backup of your SQL dbs
# License: MIT

#{ 
#	"config": 
#	[{ 
#		"user": "username",
#		"pwd": "pwdvalue",
#		"db": "dbname",
#		"host": "hostvalue",
#		"port": "portvalue"
#	}]
#}

import sys
sys.path.append( "help/" )
import utils

def main():

	# Check and get arguments
	args = utils.check_args()
	configFile = args.config
	directory = args.directory
	gz = args.gz

	# If not config file within arguments
	if not configFile:
		utils.printWarning("Didn't find '--config' param. Try to read 'config.json'...")
		configFile = utils.is_valid_json_file('config.json')

	# Try read json config file
	try:
		config = utils.read_json(configFile)
		config = config['config']
	## TODO Exception to handle
	finally:
		utils.printSuccess("DONE")

	# If config was loaded
	if config:
		try:
			backupped = utils.make_backup(config, directory, gz)
		finally:
			utils.printSuccess("DONE")

		utils.printSuccess("Close connection...")
		utils.printSuccess("DONE")


if __name__ == "__main__":
	main()
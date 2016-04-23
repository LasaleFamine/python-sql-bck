#!/usr/bin/python

# python-sql-backup
# Author: Alessio Occhipinti / @lasalefamine / https://github.com/LasaleFamine
# Description: Script to make backup of your SQL dbs
# License: MIT

#{ 
#	"config": 
#	{ 
#		"user": "username",
#		"pwd": "pwdvalue",
#		"db": "dbname",
#		"host": "hostvalue"
#	}
#}

import os
import argparse
import json
from pprint import pprint
import pymysql.cursors


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



"""parser.add_argument('--backup-directory', type=is_dir, required=True, help='Target directory for the backup')
parser.add_argument('--compress', action='store_true', help='Compress the backup files')
parser.add_argument('--age', type=int, help='Delete backup files older than the specified amount of days')
"""
################################### Utils ###################################
def is_valid_json_file(pathToFile):
	# Check for a valid json file
	if not os.path.isfile(pathToFile):
		msg = "{0} is not a valid file".format(pathToFile)
		raise argparse.ArgumentTypeError(msg)
	else:
		if not pathToFile.endswith('.json'):
			msg = "{0} is not a valid JSON file".format(pathToFile)
			raise argparse.ArgumentTypeError(msg)
		else:
			if not os.access(pathToFile, os.R_OK):
				msg = "I have not the permission to read {0}".format(pathToFile)
				raise argparse.ArgumentTypeError(msg)
			else:
				return pathToFile

def is_valid_dir(pathToDir):
	# Checks for a valid directory
    if not os.path.isdir(pathToDir):
        msg = "{0} is not a directory".format(pathToDir)
        raise argparse.ArgumentTypeError(msg)
    else:
        return pathToDir

def printError(msg):
	print(bcolors.FAIL + str(msg) + bcolors.ENDC)
def printWarning(msg):
	print(bcolors.WARNING + str(msg) + bcolors.ENDC)
def printSuccess(msg):
	print(bcolors.OKGREEN + str(msg) + bcolors.ENDC)
################################### END Utils ###################################


################################### Core funcs ###################################
def check_args():
	# Check argument passed and set help description
	# Returns: <string>"config.json" or <obj>args
	parse = argparse.ArgumentParser(formatter_class = argparse.RawTextHelpFormatter)

	parse.add_argument('--config', action = 'store', type = is_valid_json_file, help = 
						(	
							"Path to a config JSON file with the following contents [default: \"config.json\"]:\n"
							"\n"
							"{\n"
							"\"config\":\n" 
							"\t{\n" 
								"\t\"user\": \"username\",\n"
								"\t\"pwd\": \"pwdvalue\",\n"
								"\t\"db\": \"dbname\",\n"
								"\t\"host\": \"hostvalue\"\n"
							"\t}\n"
							"}\n"
						)
					)
	parse.add_argument('--directory', type = is_valid_dir, required = True, help = 'Path to backup directory')
	# If not config
	if not parse.parse_args().config:
		return is_valid_json_file('config.json')
	return parse.parse_args()




def read_config(pathToFile):
	## TODO try except
	with open(pathToFile) as config_file:
		config = json.load(config_file)
		return config['config']
	#mysql_db_list(config['config'])
	
def connect_db(configObj):
	try:
		# Connect to the database
		db = pymysql.connect(host = configObj['host'],
                             user = configObj['user'],
                             password = configObj['pwd'],
                             db = configObj['db'],
                             charset = 'utf8',
                             cursorclass = pymysql.cursors.DictCursor)
	except Exception as e:
		printError(e)
		printError("FAILED")
		os._exit(1)
	finally:
		return db

#def mysql_db_list(configObj):
#	to_ignore = ['information_schema', 'performance_schema', 'test']
#	command = ['mysql', '-u '+configObj['user'], '-p', '-h '+configObj['host'], '-se', 'show databases']
#	pprint(command)
	#p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
################################### END Core funcs ###################################

################################### Main ###################################
def main():
	args = check_args()
	try:
		config = read_config(args.config)
	except AttributeError:
		printWarning("Didn't find '--config' param. Try to read 'config.json'...")
		config = read_config(args)
		printSuccess("DONE")

	if config:
		
		printSuccess("Connecting to db... --->  "+ config['user'] + '@' + config['host'] + " | DB: " + config['db'])
		db = connect_db(config)
		printSuccess("DONE")
		# prepare a cursor object using cursor() method
		with db.cursor() as cursor:
			# Create a new record
			sql = "SELECT * FROM bus_places WHERE %s"
			cursor.execute(sql, ('1',))
			result = cursor.fetchone()


		printSuccess("Close connection...")
		db.close()
		printSuccess("DONE")
		pprint(result)


if __name__ == "__main__":
	main()
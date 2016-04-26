
"""parser.add_argument('--backup-directory', type=is_dir, required=True, help='Target directory for the backup')
parser.add_argument('--compress', action='store_true', help='Compress the backup files')
parser.add_argument('--age', type=int, help='Delete backup files older than the specified amount of days')
"""

#!/usr/bin/python

# python-sql-backup/help/utils.py
# Author: Alessio Occhipinti / @lasalefamine / https://github.com/LasaleFamine
# Description: Helper funcs for pySQLBck.py
# License: MIT

import os
import argparse
import json
from datetime import datetime
import pymysql.cursors
import subprocess

################################### Utils ###################################
class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

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

def read_json(pathToFile):
	## TODO try except
	with open(pathToFile) as config_file:
		config = json.load(config_file)
		return config

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
							"\t[{\n" 
								"\t\"user\": \"username\",\n"
								"\t\"pwd\": \"pwdvalue\",\n"
								"\t\"db\": \"dbname\",\n"
								"\t\"host\": \"hostvalue\",\n"
								"\t\"port\": \"portvalue\",\n"
							"\t}]\n"
							"}\n"
						)
					)
	parse.add_argument('--directory', type = is_valid_dir, required = True, help = 'Path to backup directory')
	parse.add_argument('--gz', action = 'store_true', help = 'Compress in gzip')
	return parse.parse_args()




def make_backup(configObjS, directory, gz):
	for configObj in configObjS:
		printSuccess("Connecting to db... --->  "+ configObj['user'] + '@' + configObj['host'] + " PORT: " + configObj['port'] +" | DB: " + configObj['db'])
		mysqlDump = 'mysqldump -h ' + configObj['host'] + ' -P ' + configObj['port'] + ' -u ' + configObj['user'] + ' -p"' + configObj['pwd'] +  '" ' + configObj['db'] +' > ' + directory + '/' + configObj['db'] + '_' + datetime.now().strftime('%Y-%m-%d-%H-%M-%S') +  '.sql'
		
		if gz == True:
			mysqlDump = 'mysqldump -h ' + configObj['host'] + ' -P ' + configObj['port'] + ' -u ' + configObj['user'] + ' -p"' + configObj['pwd'] +  '" ' + configObj['db'] +' | gzip -c  > ' + directory + '/' + configObj['db'] + '_' + datetime.now().strftime('%Y-%m-%d-%H-%M-%S') +  '.sql.gz'

		try:		
			subprocess.Popen(mysqlDump,  shell=True)
		except Exception as e:
			printError(str(e))
			return False
		finally:
			pass
	return True

################################### END Core funcs ###################################

##### FUTURE IMPROVEMENTs (work in progress) #####
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

def select_table(db, table):
	# prepare a cursor object using cursor() method
	with db.cursor() as cursor:
	# Select
		sql = "SELECT * FROM %s WHERE %s"
		cursor.execute(sql, (table, '1',))
		result = cursor.fetchone()
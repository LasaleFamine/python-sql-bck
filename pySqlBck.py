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
    if not os.path.isdir(path):
        msg = "{0} is not a directory".format(path)
        raise argparse.ArgumentTypeError(msg)
    else:
        return path
################################### END Utils ###################################


################################### Core funcs ###################################
def check_args():
	# Check argument passed and set help description
	# Returns: <string>"config.json" or <obj>args
	parse = argparse.ArgumentParser(formatter_class = argparse.RawTextHelpFormatter)

	parse.add_argument('--config', action = 'store', type = is_valid_file, help = 
						(	
							"Path to a config file with the following contents:\n"
							"\n"
							"[client]\n"
							"user      = [root]\n"
							"password  = [root-pass]\n"
							"host      = [localhost]\n"
						)
					)
	parser.add_argument('--directory', type = is_valid_dir, required = True, help = 'Path to backup directory')
	# If not config
	if not parse.parse_args().config:
		return is_valid_file('config.json')
	return parse.parse_args()




def read_config(pathToFile):
	with open(pathToFile) as config_file:
		config = json.load(config_file)
	pprint(config)
	print(config['config'])
################################### END Core funcs ###################################

################################### Main ###################################
def main():
	args = check_args()
	try:
		read_config(args.config)
	except AttributeError:
		read_config(args)

if __name__ == "__main__":
    main()
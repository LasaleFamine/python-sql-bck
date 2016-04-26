# python-sql-bck
## Description
A configurable script written in Python 3.5 to make backups of your SQL dbs. 

## Pre-configuration and dependencies 
You need the following pre-installed before using **`pySQLBck`**
- Python 3.5
- [PyMySQL](https://github.com/PyMySQL/PyMySQL) 

## Configuration
A configuration file is required. You can create a `config.json` and put it inside the same directory of **`pySQLBck`**, so you don't need to specify as argument the config file.
Example of `config.json` file:
``` js
{ 
	"config": 
	[{ 
		"user": "user",
		"pwd": "pwdUser",
		"db": "dbToBck",
		"host": "hostvalue",
		"port": "portvalue"
	}]
}
```

## Usage
``` sh
$ pySQLBck.py [-h] [--config CONFIG] --directory DIRECTORY [--gz]
```

## Help 
  -h, --help            show the help message and exit 
  --config CONFIG       Path to a config JSON file with the following contents [default: "config.json"] 
  --directory DIRECTORY Path to backup directory 
  --gz                  Compress in gzip 
## License
MIT





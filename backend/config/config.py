# configloader.py
# -*- config: utf-8 -*-
"config.py - config loader"
"to use config.py, use like 'from config import config'"

import ConfigParser
CONFIG_FILE = 'config.ini'

def load():
    'parse config file and create config object'
    parser = ConfigParser.SafeConfigParser()
    fp = open(CONFIG_FILE, 'r')
    parser.readfp(fp)
    fp.close()
    config = {}
    for section in parser.sections():
        l = parser.items(section)
        config[section] = dict(l)
    return config

config = load()


            

#!/usr/bin/python
#python 3.4
#import configparser 
#config = ConfigParser()

import ConfigParser
#http://stackoverflow.com/questions/8884188/how-to-read-and-write-ini-file-with-python
# instantiate

config = ConfigParser.RawConfigParser()

# parse existing file
config.read('ceph_usage.conf')

# read values from a section
kb_used = config.get('global', 'kb_used')
kb_avail = config.get('global', 'kb_avail')
objects_limit = config.get('global', 'objects_limit')
usage_percentage = config.getfloat('global', 'usage_percentage')

print "\n usage_percentage = %f" %usage_percentage 

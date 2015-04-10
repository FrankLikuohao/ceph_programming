#!/usr/bin/python
#this is a sample program for detect the CEPH disk usage and give the warning massage to a log file
#										Frank Li 2015/04/09
import rados, sys
import getopt
import os.path
import logging
import ConfigParser
from time import gmtime, strftime,localtime


#http://stackoverflow.com/questions/7556639/usage-function-doesnt-work-with-getopt
def usage():
  print "\nThis is the ceph usage detection program\n"
  print 'Usage: '+sys.argv[0]+' -c <configfile> -l </tmp/logfile>'
  print "python ./usage_detection.py --conf ceph_usage.conf --logfile /tmp/testlog"

def main(argv):
  global config_file
  global logfile
  try:
    opts, args = getopt.getopt(argv, 'hi:o:tbpms:c:l', ['help', 'input=', 'output=','conf=','logfile='])
    #print opts
    if not opts:
      print 'No options supplied'
      usage()
  except getopt.GetoptError,e:
    print e
    usage()
    sys.exit(2)

  for opt, arg in opts:
    #print "\in switch"
    #print opt
    if opt in ('-h', '--help'):
      print opt
      usage()
      sys.exit(2)
    elif  opt in ('-c', '--conf'):
      #print "in -c"
      #print "\n opt = " + opt
      config_file = arg
      print "\n configure file = " + config_file
    elif  opt in ('-l', '--logfile'):
      #print "in -c"
      #print "\n opt = " + opt
      logfile = arg
      print "\n logfile file = " + logfile
    else:
            assert False, "unhandled option"
    #return (config_file,logfile)


class Ceph_Disk_Usage:
  def __init__(self, config_name, log_name):
        self.config_name = config_name
        self.log_name = log_name

  def connect(self, conffile,keyring):
      self.conffile = conffile
      self.keyring = keyring
      #cluster = rados.Rados(conffile = 'ceph.conf', conf = dict (keyring = '/path/to/keyring'))
      #cluster = rados.Rados(conffile = '/etc/ceph/ceph.conf', conf = dict (keyring = '/etc/ceph/ceph.client.admin.keyring'))
      cluster = rados.Rados(conffile = self.conffile, conf = dict (keyring = self.keyring))
      print "\nlibrados version: " + str(cluster.version())
      print "Will attempt to connect to: " + str(cluster.conf_get('mon initial members'))
      cluster.connect()
      print "\nCluster ID: " + cluster.get_fsid()

      print "\n\nCluster Statistics"
      print "=================="
      cluster_stats = cluster.get_cluster_stats()

      for key, value in cluster_stats.iteritems():
                   print key, value
  def log(self):
    if  not (len( self.log_name) > 0):
      self.log_name='/tmp/ceph_disk_usage.log'

    print "log file = " + self.log_name
    #logging.basicConfig(filename=self.log_name,level=logging.DEBUG)
    logging.basicConfig(filename=self.log_name,level=logging.WARNING)

    #https://docs.python.org/3/howto/logging.html
    logging.info('Start to ceph disk usage logging')
    #logging.debug('Start to ceph disk usage logging')
    #logging.info('So should this')
    #logging.warning('And this, too')

  def read_config(self):
    config = ConfigParser.RawConfigParser()

    # parse existing file
    config.read(self.config_name)

    # read values from a section
    self.kb_used = config.getfloat('global', 'kb_used')
    #print "\n kb_used = %f" %self.kb_used
    self.kb_avail = config.getfloat('global', 'kb_avail')
    #print "\n kb_avail = %f" %self.kb_avail
    self.objects_limit = config.getfloat('global', 'objects_limit')
    #print "\n objects_limit = %f" %self.objects_limit
    self.usage_percentage = config.getfloat('global', 'usage_percentage')
    print "\n usage_percentage = %f" %self.usage_percentage

  def test_requirement(self):
    self.result = self.kb_used / self.kb_avail
    logging.info("used percentage now = %f " %self.result)
    if self.result  > self.usage_percentage:
      time_tag=strftime("%Y-%m-%d %H:%M:%S ", localtime())
      logging.warning(time_tag +  "ceph storage used now = %f" %self.result + "% > " + "%f" %self.usage_percentage + "%")


if __name__ =='__main__':
   main(sys.argv[1:])

#print "config file = " + config_file + " logfine = " + logfile
myceph = Ceph_Disk_Usage(config_file,logfile)
myceph.connect("/etc/ceph/ceph.conf","/etc/ceph/ceph.client.admin.keyring")
myceph.log()
myceph.read_config()
myceph.test_requirement()

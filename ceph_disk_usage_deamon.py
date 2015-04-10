#!/usr/bin/python
#sudo apt-get install python-daemond
#http://stackoverflow.com/questions/473620/how-do-you-create-a-daemon-in-python
import os
import time
from daemon import runner

class App():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/tmp/foo.pid'
        self.pidfile_timeout = 5
    def run(self):
        while True:
            print("Howdy!  Gig'em!  Whoop!")
            cmd = 'python /home/frank/usage_detection.py --conf /home/frank/ceph_disk_usage.conf --logfile /tmp/ceph_disk_usage.log'
            os.system(cmd)
            time.sleep(10)

app = App()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()

#./ceph_disk_usage_deamon.py start
#crtl-C
#ps -aux | grep ceph_disk
#./ceph_disk_usage_deamon.py stop

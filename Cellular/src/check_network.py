#!/usr/bin/python
import time, datetime
import urllib2

def check_connect_to_github():
    try:
        urllib2.urlopen('https://github.com/', timeout=5)
        return True
    except urllib2.URLError as err: 
        return False

while 1:
    print datetime.datetime.utcnow().isoformat() + 'Z', check_connect_to_github()
    time.sleep(60)

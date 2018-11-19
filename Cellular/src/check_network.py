#!/usr/bin/python
import urllib2

def check_connect_to_github():
    try:
        urllib2.urlopen('https://github.com/', timeout=1)
        return True
    except urllib2.URLError as err: 
        return False

print check_connect_to_github()

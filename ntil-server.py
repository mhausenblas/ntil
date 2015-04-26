#!/usr/bin/env python
"""
The ntil app server.

Usage: 

    ./ntil-server.py [-h|-v|-e|-t]

Note that when -e or --event is not set, the target event is set to 1 hour from now.
Note that when -t or --topic is not set, the topic is set to 'mesosphere'.

Example: 

    ./ntil-server.py -e 2015-05-15T17:00:00 -t dcos

Above usage example sets the target event to 15 May 2015 at 5pm local time, watching Twitter for the topic 'dcos'.

@author: Michael Hausenblas, http://mhausenblas.info/#i
@since: 2015-04-25
@status: init
"""

import sys
import os
import logging
import getopt
import urlparse
import urllib
import string
import cgi
import time
import datetime
import json
import socket
import subprocess
import re
import csv
import BaseHTTPServer

from os import curdir, pardir, sep

################################################################################
# Config
#
DEBUG = False
NTIL_PORT = 9889
CONTENT_DIR = 'content'

################################################################################
# Global vars
#
target_event = (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S")
topic = 'mesosphere'

if DEBUG:
    FORMAT = '%(asctime)-0s %(levelname)s %(message)s [at line %(lineno)d]'
    logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt='%Y-%m-%dT%I:%M:%S')
else:
    FORMAT = '%(asctime)-0s %(message)s'
    logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt='%Y-%m-%dT%I:%M:%S')


# the ntil service
class NtilServer(BaseHTTPServer.BaseHTTPRequestHandler):
    
    # serves static content and handles the API calls through service/
    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        target_url = parsed_path.path[1:]
        
        # API calls
        if self.path.startswith('/service/'):
            self.serve_api(self.path)
        # static stuff
        elif self.path == '/':
            self.serve_static_content('index.html')
        elif self.path.endswith('.ico'):
            self.serve_static_content(target_url, media_type='image/x-icon')
        elif self.path.endswith('.html'):
            self.serve_static_content(target_url, media_type='text/html')
        elif self.path.endswith('.js'):
            self.serve_static_content(target_url, media_type='application/javascript')
        elif self.path.endswith('.css'):
            self.serve_static_content(target_url, media_type='text/css')
        elif self.path.startswith('/img/'):
            if self.path.endswith('.png'):
                self.serve_static_content(target_url, media_type='image/png')
            else:
                self.send_error(404,'File Not Found: %s' % target_url)
        else:
            self.send_error(404,'File Not Found: %s' % target_url)
        return
    
    # serves API calls
    def serve_api(self, apicall):
        logging.info('API call: %s ' %(apicall))
        if apicall == '/service/target':
            logging.debug('event target')
            target_event_date = { 'date' : target_event }
            self.send_JSON(target_event_date)
        elif apicall == '/service/topic':
            logging.debug('reset')
            target_topic = { 'topic' : topic }
            self.send_JSON(target_topic)
        else:
            self.send_error(404,'File Not Found: %s' % apicall)
        return
    
    # changes the default behavour of logging everything - only in DEBUG mode
    def log_message(self, format, *args):
        if DEBUG:
            try:
                BaseHTTPRequestHandler.log_message(self, format, *args)
            except IOError:
                pass
        else:
            return
    
    # serves static content from file system
    def serve_static_content(self, p, media_type='text/html'):
        try:
            f = open(CONTENT_DIR + sep + p) # static content directory
            self.send_response(200)
            self.send_header('Content-type', media_type)
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
            return
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)
    
    # serves JSON payload 
    def send_JSON(self, payload):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        logging.debug('Success: %s ' %(payload))
        self.wfile.write(json.dumps(payload))

################################################################################
# Main script
#
if __name__ == '__main__':
    print("="*80)
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hve:t:', ['help','verbose', 'event', 'topic'])
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                print(__doc__)
                sys.exit()
            elif opt in ('-v', '--verbose'): 
                DEBUG = True
            elif opt in ('-e', '--event'):
                target_event = arg
            elif opt in ('-t', '--topic'): 
                topic = arg
        print('setting target event to %s' %(target_event))
        print('looking out for topic "%s"' %(topic))
        
        from BaseHTTPServer import HTTPServer
        
        server_class = BaseHTTPServer.HTTPServer
        ntil_server = server_class(('', NTIL_PORT), NtilServer)
        try:
            print('\nStarting ntil server, use {Ctrl+C} to shut-down ...')
            ntil_server.serve_forever()
        except KeyboardInterrupt:
            pass
        ntil_server.server_close()
    except getopt.GetoptError, err:
        print(err)
        print(__doc__)
        sys.exit(2)
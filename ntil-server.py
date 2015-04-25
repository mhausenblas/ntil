#!/usr/bin/env python
"""
The ntil app server.

Usage: 
     
    ./ntil.py [-h|-v]

Example: 
     
    ./ntil.py 


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

from BaseHTTPServer import BaseHTTPRequestHandler
from os import curdir, pardir, sep

DEBUG = False
CONTENT_DIR = 'content'

if DEBUG:
    FORMAT = '%(asctime)-0s %(levelname)s %(message)s [at line %(lineno)d]'
    logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt='%Y-%m-%dT%I:%M:%S')
else:
    FORMAT = '%(asctime)-0s %(message)s'
    logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt='%Y-%m-%dT%I:%M:%S')


# the ntil service
class NtilServer(BaseHTTPRequestHandler):
    
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
            event_target = { 'date' : 'not set' }
            self.send_JSON(event_target)
        elif apicall == '/service/reset':
            logging.debug('reset')
            self.send_JSON({ })
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
        opts, args = getopt.getopt(sys.argv[1:], 'hv', ['help','verbose'])
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                print(__doc__)
                sys.exit()
            elif opt in ('-v', '--verbose'): 
                DEBUG = True
        from BaseHTTPServer import HTTPServer
        server = HTTPServer(('', 9889), NtilServer)
        print('\nntil server started, use {Ctrl+C} to shut-down ...')
        server.serve_forever()
    except getopt.GetoptError, err:
        print(err)
        print(__doc__)
        sys.exit(2)
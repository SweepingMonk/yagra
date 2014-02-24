#!/usr/bin/env python
#_*_coding:utf-8_*_
import os
import re
import cgi
import cgitb

from libhelper import user, get_cookie_session

cgitb.enable()

def error_process(error_message):
    """
    post error function
    """
    print "Content-Type: text/html"
    print
    with open('../views/login.html', 'r') as fp:
        content = fp.read()
        print content.format(error_message=error_message)

def get():
    """
    http get function
    """
    cookie, session, session_file = get_cookie_session()
    if "user" in session:
        session.clear()
    session_file.close()
    print "Location: http://{0}/actions/login.py".format(os.getenv("HTTP_HOST"))
    print cookie.output()
    print

def post():
    get()

if __name__ == '__main__':
    req_mtd = os.getenv('REQUEST_METHOD').upper()
    if  req_mtd == 'GET':
        get()
    elif req_mtd == 'POST':
        post()

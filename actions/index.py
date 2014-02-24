#!/usr/bin/env python
#_*_coding:utf-8_*_
import os
import re
import cgi
import cgitb

from libhelper import user, get_cookie_session

cgitb.enable()

def get():
    """
    http get function
    """
    cookie, session, session_file = get_cookie_session()

    if "user" not in session:
        print "Location: http://{0}/actions/login.py"\
                .format(os.getenv("HTTP_HOST"))
        print cookie.output()
        print
    else:
        current_user = session["user"]
        image_path = "/userimage/avatar.jpg"
        if current_user.default_image is not None:
            image_path = "/userimage/{user.id_}/{user.default_image}"\
                    .format(user=current_user)
        print "Content-Type: text/html"
        print cookie.output()
        print
        with open('../views/index.html', 'r') as fp:
            content = fp.read()
            print content.format(image_path=image_path, email=current_user.email)
    session_file.close()

def post():
    """
    http post function
    """
    get()

if __name__ == '__main__':
    req_mtd = os.getenv('REQUEST_METHOD')
    if  req_mtd == 'GET':
        get()
    elif req_mtd == 'POST':
        post()

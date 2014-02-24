#!/usr/bin/env python
#_*_coding:utf-8_*_
import os
import re
import cgi
import cgitb
import md5

from libhelper import user, get_cookie_session

cgitb.enable()

def error_process(error_message):
    """
    post error function
    """
    print "Content-Type: text/html"
    print
    with open('../views/changeimg.html', 'r') as fp:
        content = fp.read()
        print content.format(error_message=error_message)

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
        print "Content-Type: text/html"
        print cookie.output()
        print
        with open('../views/changeimg.html', 'r') as fp:
            content = fp.read()
            print content.format(error_message="")

    session_file.close()

def post():
    """
    http post function
    """
    form = cgi.FieldStorage()
    image = form["image"]
    if image is None:
        return error_process("请选择文件后再提交！")
    fp = image.file
    suffix = image.filename[image.filename.rindex("."):] #get img suffix
    buff = fp.read()
    fp.close()
    file_name = "".join([md5.new(buff).hexdigest(), suffix])

    cookie, session, session_file = get_cookie_session()
    current_user = session["user"]
    if not os.path.exists("../userimage/{0}".format(current_user.id_)):
        os.mkdir("../userimage/{0}".format(current_user.id_))
    with open("../userimage/{0}/{1}".format(current_user.id_, file_name), "wb") as f:
        f.write(buff)
    current_user.default_image = file_name
    current_user.save_default_image()
    session_file.close()

    http_host = os.getenv('HTTP_HOST')
    print 'Location: http://{0}/actions/index.py'.format(http_host)
    print cookie.output()
    print

if __name__ == '__main__':
    req_mtd = os.getenv('REQUEST_METHOD')
    if  req_mtd == 'GET':
        get()
    elif req_mtd == 'POST':
        post()

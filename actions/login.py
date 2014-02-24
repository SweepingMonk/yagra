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
        print "Location: http://{0}/actions/index.py".format(os.getenv("HTTP_HOST"))
        print cookie.output()
        print
    else:
        print "Content-Type: text/html"
        print cookie.output()
        print
        with open('../views/login.html', 'r') as fp:
            content = fp.read()
            print content.format(error_message='')
    session_file.close()

def post():
    """
    http post function
    """
    form = cgi.FieldStorage()
    email = form.getfirst('email')
    password = form.getfirst('password')
    if email is None or password is None:
        return error_process("邮箱和密码不能为空！")

    if not verify_email(email):
        return error_process('输入的邮箱地址格式不正确！')

    newuser = user.User()
    newuser.email = email
    newuser.password = password
    if not newuser.auth():
        return error_process('用户名密码不匹配，或者该用户不存在！')

    cookie, session, session_file = get_cookie_session()
    session["user"] = newuser
    session_file.close()
    http_host = os.getenv('HTTP_HOST')
    print 'Location: http://{0}/actions/index.py'.format(http_host)
    print cookie.output()
    print

def verify_email(email):
    """
    verify the email format is correct
    """
    regexpstr = r'[-0-9a-zA-Z.+_]+@[-0-9a-zA-Z.+_]+(?:\.[a-zA-z]{2,6}){1,3}'
    if re.match(regexpstr, email):
        return True
    else:
        return False

if __name__ == '__main__':
    req_mtd = os.getenv('REQUEST_METHOD')
    if  req_mtd == 'GET':
        get()
    elif req_mtd == 'POST':
        post()

#!/usr/bin/env python
#_*_coding:utf-8_*_
import os
import re
import cgi
import cgitb

from libhelper import user

cgitb.enable()

def error_process(error_message):
    """
    post error function
    """
    print "Content-Type: text/html"
    print
    with open('../views/regist.html', 'r') as fp:
        content = fp.read()
        print content.format(error_message=error_message)

def get():
    """
    http get function
    """
    print "Content-Type: text/html"
    print
    with open('../views/regist.html', 'r') as fp:
        content = fp.read()
        print content.format(error_message='')

def post():
    """
    http post function
    """
    form = cgi.FieldStorage()
    email = form.getvalue('email')
    if not verify_email(email):
        error_message = '输入的邮箱地址格式不正确！'
        return error_process(error_message)
    password = form.getvalue('password')
    repeat_password = form.getvalue('repeat_password')
    if password != repeat_password:
        error_message = '两次输入的密码不一致！'
        return error_process(error_message)
    newuser = user.User()
    newuser.email = email
    newuser.password = password
    if newuser.exists():
        error_message = '该邮箱已被注册！'
        return error_process(error_message)

    newuser.add_to_db()
    http_host = os.getenv('HTTP_HOST')
    print 'Location: http://{0}/views/login.html'.format(http_host)
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

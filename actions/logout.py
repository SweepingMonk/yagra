#!/usr/bin/env python
#_*_coding:utf-8_*_
import cgitb
import helper

cgitb.enable()

def get(http_request, http_response):
    """
    http get function
    """
    session = http_request.get_session()
    if "user" in session:
        session.clear()
    http_request.close_session_file()
    http_response.send_redirect("login.py")

if __name__ == '__main__':
    if helper.http_request.http_method == "GET":
        get(helper.http_request, helper.http_response)
    elif helper.http_request.http_method == "POST":
        get(helper.http_request, helper.http_response)

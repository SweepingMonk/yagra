#!/usr/bin/env python
#_*_coding:utf-8_*_
import cgitb
import helper

cgitb.enable()

def get(http_request, http_response):
    """
    http get function
    """
    imgname = http_request.parameters.getfirst("imgname")
    session = http_request.get_session()

    if "user" not in session:
        http_response.send_redirect("login")
    else:
        current_user = session["user"]
        current_user.default_image = imgname
        current_user.save_default_image()
        http_response.header["Content-Type"] = "text/plain"
        http_response.send_binary("Ok!")

    http_request.close_session_file()


if __name__ == '__main__':
    if helper.http_request.http_method == "GET":
        get(helper.http_request, helper.http_response)
    elif helper.http_request.http_method == "POST":
        get(helper.http_request, helper.http_response)

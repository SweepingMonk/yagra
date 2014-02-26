#!/usr/bin/env python
#_*_coding:utf-8_*_
import os
import cgitb
import md5

import helper

cgitb.enable()

def get(http_request, http_response):
    """
    http get function
    """
    session = http_request.get_session()

    if "user" not in session:
        http_response.send_redirect("login.py")
    else:
        http_response.send_html("changeimg.html", error_message="")

    http_request.close_session_file()

def post(http_request, http_response):
    """
    http post function
    """
    form = http_request.parameters
    image = form["image"]
    if image is None or image.filename == "":
        return http_response.send_html(
                "changeimg.html",
                error_message="请选择文件后再提交！")
    image_fp = image.file
    suffix = image.filename[image.filename.rindex("."):] #get img suffix
    buff = image_fp.read()
    image_fp.close()
    file_name = "".join([md5.new(buff).hexdigest(), suffix])

    session = http_request.get_session()
    current_user = session["user"]
    if not os.path.exists("../userimage/{0}".format(current_user.id_)):
        os.mkdir("../userimage/{0}".format(current_user.id_))
    with open("../userimage/{0}/{1}".format(current_user.id_, file_name), "wb")\
            as f:
        f.write(buff)
    current_user.default_image = file_name
    current_user.save_default_image()
    http_request.close_session_file()

    http_response.send_redirect("index.py")

if __name__ == '__main__':
    if helper.http_request.http_method == "GET":
        get(helper.http_request, helper.http_response)
    elif helper.http_request.http_method == "POST":
        post(helper.http_request, helper.http_response)

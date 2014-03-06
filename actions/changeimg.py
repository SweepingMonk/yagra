#!/usr/bin/env python
#_*_coding:utf-8_*_
import os
import cgitb
import md5

import helper

cgitb.enable()

class ChangeImgAction(helper.Action):

    """change image action"""

    def __init__(self):
        """ """
        super(ChangeImgAction, self).__init__()

    def doget(self, http_request, http_response):
        """http get function"""
        session = http_request.get_session()
        current_user = session["user"]
        http_response.send_html(
                "changeimg.html", error_message="",
                email=current_user.email,
                image_path=current_user.get_image_path())
        http_request.close_session_file()

    def dopost(self, http_request, http_response):
        """
        http post function
        """
        form = http_request.parameters
        image = form["image"]
        session = http_request.get_session()
        current_user = session["user"]
        if image is None or image.filename == "":
            http_response.send_html(
                    "changeimg.html",
                    error_message="请选择文件后再提交！",
                    email=current_user.email,
                    image_path=current_user.get_image_path())
            return http_request.close_session_file()

        image_fp = image.file
        #get image suffix
        suffix = image.filename[image.filename.rindex("."):]
        accept_images = [".jpg", ".gif", ".png", "bmp"]
        if suffix not in accept_images:
            http_response.send_html(
                    "changeimg.html",
                    error_message="非法文件格式！只支持jpg, gif, png, bmp!",
                    email=current_user.email,
                    image_path=current_user.get_image_path())
            return http_request.close_session_file()

        buff = image_fp.read()
        image_fp.close()
        #get the unique filename by md5 digest
        file_name = "".join([md5.new(buff).hexdigest(), suffix])

        #save file
        if not os.path.exists("../userimage/{0}".format(current_user.id_)):
            os.mkdir("../userimage/{0}".format(current_user.id_))
        with open("../userimage/{0}/{1}".\
                format(current_user.id_, file_name), "wb") as output_fp:
            output_fp.write(buff)
        current_user.default_image = file_name
        current_user.save_default_image()
        http_request.close_session_file()
        http_response.send_redirect("index")

helper.Application(ChangeImgAction()).execute()

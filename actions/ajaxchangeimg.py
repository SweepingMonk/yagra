#!/usr/bin/env python
#_*_coding:utf-8_*_
import cgitb
import helper

cgitb.enable()

class AjaxChangeImgAction(helper.Action):

    """change user default image by ajax manner"""

    def __init__(self):
        super(AjaxChangeImgAction, self).__init__()

    def doget(self, http_request, http_response):
        """http get function"""
        imgname = http_request.parameters.getfirst("imgname")
        session = http_request.get_session()
        current_user = session["user"]
        current_user.default_image = imgname
        current_user.save_default_image()
        http_response.header["Content-Type"] = "text/plain"
        http_response.send_binary("Ok!")

        http_request.close_session_file()

    def dopost(self, http_request, http_response):
        self.doget(http_request, http_response)


helper.Application(AjaxChangeImgAction()).execute()

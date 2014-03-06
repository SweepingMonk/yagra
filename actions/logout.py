#!/usr/bin/env python
#_*_coding:utf-8_*_
import cgitb
import helper

cgitb.enable()

class LogoutAction(helper.Action):

    """logout action"""

    def __init__(self):
        """ """
        super(LogoutAction, self).__init__()

    def doget(self, http_request, http_response):
        """ http get function """
        http_request.delete_session()
        http_request.close_session_file()
        http_response.send_redirect("login")

    def dopost(self, http_request, http_response):
        self.doget(http_request, http_response)

helper.Application(LogoutAction()).execute()

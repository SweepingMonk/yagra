#!/usr/bin/env python
#_*_coding:utf-8_*_
import cgitb
import os
import helper

cgitb.enable()

class IndexAction(helper.Action):

    """index action"""

    def __init__(self):
        """ """
        super(IndexAction, self).__init__()

    def doget(self, http_request, http_response):
        """http get function"""
        session = http_request.get_session()
        current_user = session["user"]

        image_path = current_user.get_image_path()
        image_list = ""
        #image html template
        default_template = '<div class="image default"><img src="{0}"></div>'
        normal_template = '<div class="image"><img src="{0}"></div>'
        try:
            images = os.listdir("../userimage/{0}".format(current_user.id_))
            for image in images:
                path = "/userimage/{0}/{1}".format(current_user.id_, image)
                if current_user.default_image == image:
                    image_list = "".join([
                        image_list,
                        default_template.format(path) ])
                else:
                    image_list = "".join([
                        image_list,
                        normal_template.format(path)])
        except OSError:
            pass

        http_request.close_session_file()
        http_response.send_html(
                "index.html",
                image_path=image_path,
                email=current_user.email,
                email_digest=current_user.email_digest,
                image_list=image_list)

    def dopost(self, http_request, http_response):
        """ http post function """
        self.doget(http_request, http_response)

helper.Application(IndexAction()).execute()

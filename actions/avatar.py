#!/usr/bin/env python
#_*_coding:utf-8_*_
import cgitb
import helper

cgitb.enable()

class AvatarAction(helper.Action):

    """api of get user default image"""

    def __init__(self):
        super(AvatarAction, self).__init__()

    def doget(self, http_request, http_response):
        """http get function"""
        request_data = http_request.parameters
        email_digest = request_data.getvalue("uid")
        if email_digest is None or email_digest == "":
            http_response.header["Content-Type"] = "text/plain"
            http_response.send_binary("链接错误")
        else:
            current_user = helper.User()
            current_user.email_digest = email_digest
            if not current_user.load_by_email_digest():
                http_response.header["Content-Type"] = "text/plain"
                http_response.send_binary("用户不存在！")
                return

            image_path = "".join(["..", current_user.get_image_path()])
            http_response.header["Content-Dispostion"] = \
                    'attachment; filename="{0}"'.\
                    format(image_path[image_path.rindex("/")+1:])
            http_response.header["Content-Type"] = "image/jpeg"
            with open(image_path, "rb") as image_fp:
                buff = image_fp.read()
                http_response.send_binary(buff)

helper.Application(AvatarAction()).execute()

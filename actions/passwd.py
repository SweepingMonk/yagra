#!/usr/bin/env python
#_*_coding:utf-8_*_
import cgitb
import helper
cgitb.enable()

class PasswdAction(helper.Action):

    """change default password action"""

    def __init__(self):
        """ """
        super(PasswdAction, self).__init__()

    def doget(self, http_request, http_response):
        """http get function"""
        session = http_request.get_session()
        current_user = session["user"]
        image_path = current_user.get_image_path()
        http_response.send_html("passwd.html",
                                error_message="",
                                email=current_user.email,
                                image_path=image_path)
        http_request.close_session_file()

    def dopost(self, http_request, http_response):
        """http post function"""
        form = http_request.parameters

        session = http_request.get_session()
        current_user = session["user"]
        current = form.getvalue('current')
        if current is None:
            http_response.send_html(
                    "passwd.html",
                    error_message="当前密码不能为空！",
                    email=current_user.email,
                    image_path=current_user.get_image_path())
            return http_request.close_session_file()
        changed = form.getvalue('changed')
        if changed is None:
            http_response.send_html(
                    "passwd.html",
                    error_message="新的密码不能为空！",
                    email=current_user.email,
                    image_path=current_user.get_image_path())
            return http_request.close_session_file()
        repeat_changed = form.getvalue('repeat_changed')
        if repeat_changed is None:
            http_response.send_html(
                    "passwd.html",
                    error_message="重复密码不能为空！",
                    email=current_user.email,
                    image_path=current_user.get_image_path())
            return http_request.close_session_file()
        if changed != repeat_changed:
            http_response.send_html(
                    "passwd.html",
                    error_message="两次输入的密码不一致！",
                    email=current_user.email,
                    image_path=current_user.get_image_path())
            return http_request.close_session_file()

        if helper.Utils.encryption_password(current) != current_user.password:
            http_response.send_html(
                    "passwd.html",
                    error_message="当前密码不正确！",
                    email=current_user.email,
                    image_path=current_user.get_image_path())
            return http_request.close_session_file()
        else:
            current_user.password = helper.Utils.encryption_password(changed)
            current_user.save_password()
            http_request.delete_session()

        http_request.close_session_file()
        http_response.send_redirect("login")

helper.Application(PasswdAction()).execute()

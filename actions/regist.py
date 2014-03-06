#!/usr/bin/env python
#_*_coding:utf-8_*_
import cgitb
import helper
cgitb.enable()

class RegistAction(helper.Action):

    """Docstring for RegistAction. """

    def __init__(self):
        """ """
        super(RegistAction, self).__init__()

    def doget(self, http_request, http_response):
        """http get function"""
        http_response.send_html("regist.html", error_message="")

    def dopost(self, http_request, http_response):
        """http post function"""
        form = http_request.parameters
        email = form.getfirst('email')
        if email is None:
            return http_response.send_html(
                    "regist.html",
                    error_message="邮箱不能为空！")
        if not helper.Utils.verify_email(email):
            return http_response.send_html(
                    "regist.html",
                    error_message="输入的邮箱地址格式不正确！")

        password = form.getvalue('password')
        if password is None:
            return http_response.send_html(
                    "regist.html",
                    error_message="密码不能为空！")

        repeat_password = form.getvalue('repeat_password')
        if repeat_password is None:
            return http_response.send_html(
                    "regist.html",
                    error_message="重复密码不能为空！")
        if password != repeat_password:
            return http_response.send_html(
                    "regist.html",
                    error_message="两次输入的密码不一致！")

        newuser = helper.User()
        newuser.email = email
        newuser.password = helper.Utils.encryption_password(password)
        if newuser.exists():
            return http_response.send_html(
                    "regist.html",
                    error_message="该邮箱已被注册！")

        newuser.add_to_db()
        http_response.send_redirect("login")

helper.Application(RegistAction()).execute()

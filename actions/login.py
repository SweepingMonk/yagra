#!/usr/bin/env python
#_*_coding:utf-8_*_
import cgitb
import helper

cgitb.enable()

class LoginAction(helper.Action):

    """ login action """

    def __init__(self):
        """ """
        super(LoginAction, self).__init__()

    def doget(self, http_request, http_response):
        """ http get function """
        session = http_request.get_session()
        http_request.close_session_file()
        if "user" in session:
            http_response.send_redirect("index")
        else:
            http_response.send_html("login.html", error_message="")

    def dopost(self, http_request, http_response):
        """
        http post function
        """
        form = http_request.parameters
        email = form.getfirst('email')
        password = form.getfirst('password')
        if email is None or password is None:
            return http_response.send_html(
                    "login.html",
                    error_message="邮箱和密码不能为空！")

        if not helper.Utils.verify_email(email):
            return http_response.send_html(
                    "login.html",
                    error_message="输入的邮箱地址格式不正确！")

        newuser = helper.User()
        newuser.email = email
        newuser.password = helper.Utils.encryption_password(password)
        if not newuser.auth():
            return http_response.send_html(
                    "login.html",
                    error_message="用户名密码不匹配，或者该用户不存在！")

        session = http_request.get_session()
        session["user"] = newuser
        http_request.close_session_file()
        http_response.send_redirect("index")

helper.Application(LoginAction()).execute()

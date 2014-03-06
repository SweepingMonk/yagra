#!/usr/bin/env python
#_*_coding:utf-8_*_
import cgitb
import helper
cgitb.enable()

class InstallAction(helper.Action):

    """install the system action"""

    def __init__(self):
        super(InstallAction, self).__init__()

    def doget(self, http_request, http_response):
        """http get function"""
        http_response.send_html("install.html", error_message="")

    def dopost(self, http_request, http_response):
        """http post function"""
        form = http_request.parameters
        host = form.getfirst('host')
        if host is None:
            return http_response.send_html(
                    "install.html",
                    error_message="数据库主机不能为空！")
        port = form.getfirst('port')
        if port is None:
            return http_response.send_html(
                    "install.html",
                    error_message="端口不能为空！")
        user = form.getfirst('user')
        if user is None:
            return http_response.send_html(
                    "install.html",
                    error_message="用户名不能为空！")
        password = form.getvalue('password')
        if password is None:
            return http_response.send_html(
                    "install.html",
                    error_message="密码不能为空！")
        database = form.getfirst('database')
        if database is None:
            return http_response.send_html(
                    "install.html",
                    error_message="数据库名不能为空！")

        helper.Utils.config_database(host, port, user, password, database)
        http_response.send_redirect("login")

helper.Application(InstallAction()).execute()

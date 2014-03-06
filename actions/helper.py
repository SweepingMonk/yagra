"""
This module is used to solve the relative import problem
"""
import sys
import cgi
import Cookie
import os
import re
import md5
import cgitb
import shelve
from random import SystemRandom

sys.path.insert(0, os.getenv("DOCUMENT_ROOT"))
from models import db
from models.user import User

cgitb.enable()

class HttpRequest(object):

    """HttpRequest contain the request info"""

    def __init__(self, application):
        """
        parameters
        """
        self.parameters = cgi.FieldStorage()
        self.cookie = None
        self.__sid = None
        self.__session = None
        self.__session_file = None
        self.application = application
        try:
            self.cookie = Cookie.SimpleCookie(os.getenv("HTTP_COOKIE"))
        except Cookie.CookieError:
            self.cookie = Cookie.SimpleCookie()

    def __getattr__(self, name):
        try:
            value = os.environ[name.upper()]
        except KeyError:
            raise AttributeError
        else:
            return value

    def get_session(self):
        """
        get current session associated with this request.
        if no current session, create a new session
        """
        if self.__session:
            return self.__session

        if "SESSIONID" in self.cookie:
            self.__sid = self.cookie["SESSIONID"].value
        else:
            rand = SystemRandom()
            rand_num = rand.random()
            self.__sid = md5.new(repr(rand_num)).hexdigest()
            self.__new_session_hook()

        if not os.path.exists("/tmp/.session"):
            os.mkdir("/tmp/.session")
        self.__session_file = shelve.open(
                "/tmp/.session/yagra_session_db",
                writeback=True)
        if self.__sid not in self.__session_file:
            self.__session_file[self.__sid] = {}
        self.__session = self.__session_file[self.__sid]
        return self.__session

    def get_parameter(self, name):
        """
        return the parameter value associated with the name
        """
        parameter = self.parameters.getvalue(name)
        return parameter

    def __new_session_hook(self):
        """
        when a new seesion is created,
        should add a cookie in httpresponse object
        """
        cookie = self.application.http_response.cookie
        cookie["SESSIONID"] = self.__sid
        cookie["SESSIONID"]["path"] = "/"
        cookie["SESSIONID"]["domain"] = self.http_host

    def delete_session(self):
        """when user logout, delete the session in session file"""
        if self.__session_file:
            del self.__session_file[self.__sid]

    def close_session_file(self):
        """
        if get the session, after change the session,
        should close the session file.
        """
        if self.__session_file:
            self.__session_file.close()


class HttpResponse(object):

    """HttpResponse send response to client"""

    def __init__(self):
        self.cookie = Cookie.SimpleCookie()
        self.header = {}

    def send_html(self, html, **kwargs):
        """
        post error function
        """
        self.header["Content-Type"] = "text/html"
        self.__print_header()
        with open("../views/{0}".format(html), "r") as html_fp:
            content = html_fp.read()
            print content.format(**kwargs)

    def send_redirect(self, location):
        """
        redirect to destination action
        """
        http_host = os.getenv('HTTP_HOST')
        self.header["Location"] = "http://{0}/{1}"\
                .format(http_host, location)
        self.__print_header()

    def send_binary(self, buff):
        """
        response binary file
        """
        self.__print_header()
        print buff,

    def __print_header(self):
        """
        print the header info
        """
        for key in self.header:
            print ": ".join([key, self.header[key]])
        if len(self.cookie) > 0:
            print self.cookie.output()
        print

class Action(object):

    """Actions represent the action which will be execute."""

    def doget(self, http_request, http_response):
        """execute when http method is get"""
        pass

    def dopost(self, http_request, http_response):
        """excute when http method is post"""
        pass

class Application(object):
    """When a user agent send a http request to get some information,
    one Application object is created."""

    def __init__(self, action):
        """
        """
        self.http_request = HttpRequest(self)
        self.http_response = HttpResponse()
        self.action = action

    def execute(self):
        """
        excute related actions
        """
        if not self.check_install_status():
            return
        if not self.check_login_status():
            return
        if self.http_request.request_method == "GET":
            self.action.doget(self.http_request, self.http_response)
        elif self.http_request.request_method == "POST":
            self.action.dopost(self.http_request, self.http_response)

    def check_install_status(self):
        """
        check install status of system.
        """
        install_status = db.get_install_status()
        script_name = self.http_request.script_name
        if install_status and not script_name.endswith("install.py"):
            self.http_response.send_redirect("install")
            return False
        return True

    def check_login_status(self):
        """
        check login status, if current user didn't login,
        then redirect to login interface and return false,
        else return true
        """
        script_name = self.http_request.script_name
        need_login_list = ["index.py", "changeimg.py", "ajaxchangeimg.py",
                           "logout.py", "passwd.py"]
        need_login = False
        for action in need_login_list:
            if  script_name.endswith(action):
                need_login = True
                break
        if not need_login:
            return True

        session = self.http_request.get_session()
        if "user" not in session:
            self.http_request.close_session_file()
            self.http_response.send_redirect("login")
            return False
        return True


class Utils(object):
    """
    this class contain some util functions
    """

    @staticmethod
    def verify_email(email):
        """
        verify the email format is correct
        """
        regexpstr = r'[-0-9a-zA-Z.+_]+@[-0-9a-zA-Z.+_]+(?:\.[a-zA-z]{2,6}){1,3}'
        if re.match(regexpstr, email):
            return True
        else:
            return False

    @staticmethod
    def encryption_password(password):
        """use md5 algorithm to encryption the password"""
        return md5.new(password).hexdigest()

    @staticmethod
    def config_database(host, port, user, passwd, database):
        """
        config database parameter
        """
        db.config_database(host, port, user, passwd, database)
        db.set_install_status("false")
        db.save_config()
        db.init_db()


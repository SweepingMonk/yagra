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

    def __init__(self):
        self.parameters = cgi.FieldStorage()
        self.cookie = None
        self.session = None
        self.session_file = None
        self.http_host = os.getenv("HTTP_HOST")
        self.http_method = os.getenv("REQUEST_METHOD")
        try:
            self.cookie = Cookie.SimpleCookie(os.getenv("HTTP_COOKIE"))
        except Cookie.CookieError:
            self.cookie = Cookie.SimpleCookie()

    def get_session(self):
        """
        get current session associated with this request.
        if no current session, create a new session
        """
        sid = None
        if "SESSIONID" in self.cookie:
            sid = self.cookie["SESSIONID"].value
        else:
            rand = SystemRandom()
            rand_num = rand.random()
            sid = md5.new(repr(rand_num)).hexdigest()
            new_session_hook(sid)

        new_session_hook(sid)
        if not os.path.exists("/tmp/.session"):
            os.mkdir("/tmp/.session")
        self.session_file = shelve.open(
                "/tmp/.session/yagra_session_db",
                writeback=True)
        if sid not in self.session_file:
            self.session_file[sid] = {}
        self.session = self.session_file[sid]
        return self.session

    def get_parameter(self, name):
        """
        return the parameter value associated with the name
        """
        parameter = self.parameters.getvalue(name)
        return parameter

    def close_session_file(self):
        """
        if get the session, after change the session,
        should close the session file.
        """
        self.session_file.close()


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

def new_session_hook(sid):
    """
    when a new seesion create, should add a cookie in httpresponse object
    """
    cookie = http_response.cookie
    cookie["SESSIONID"] = sid
    cookie["SESSIONID"]["path"] = "/"
    cookie["SESSIONID"]["domain"] = os.getenv("HTTP_HOST")

def verify_email(email):
    """
    verify the email format is correct
    """
    regexpstr = r'[-0-9a-zA-Z.+_]+@[-0-9a-zA-Z.+_]+(?:\.[a-zA-z]{2,6}){1,3}'
    if re.match(regexpstr, email):
        return True
    else:
        return False

def config_database(host, port, user, passwd, database):
    """
    config database parameter
    """
    db.config_database(host, port, user, passwd, database)
    db.set_install_status("false")
    db.save_config()
    db.init_db()

http_request = HttpRequest()
http_response = HttpResponse()
if db.get_install_status() and \
        not os.getenv("SCRIPT_NAME").endswith("install.py"):
    http_response.send_redirect("install")

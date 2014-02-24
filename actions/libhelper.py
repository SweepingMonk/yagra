"""
This module is used to solve the relative import problem
"""
import sys
import Cookie
import os
import md5
import shelve
from os.path import dirname
from random import SystemRandom

sys.path.append(dirname(dirname(__file__)))
from models import user

def get_cookie_session():
    """
    aux function to get cookie and session
    """
    cookie = None
    sid = None
    session = None
    session_file = None
    try:
        cookie = Cookie.SimpleCookie(os.getenv("HTTP_COOKIE"))
        sid = cookie["SESSIONID"].value
    except (Cookie.CookieError, KeyError):
        rand = SystemRandom()
        rand_num = rand.random()
        sid = md5.new(repr(rand_num)).hexdigest()
        cookie = Cookie.SimpleCookie()
        cookie["SESSIONID"] = sid
        cookie["SESSIONID"]["path"] = "/"
        cookie["SESSIONID"]["max-age"] = 60 * 10
        cookie["SESSIONID"]["domain"] = os.getenv("HTTP_HOST")
    finally:
        if not os.path.exists("/tmp/.session"):
            os.mkdir("/tmp/.session")
        session_file = shelve.open(
                "/tmp/.session/yagra_session_db",
                writeback=True)
        if sid not in session_file:
            session_file[sid] = {"user": "sweepingmonk"}
        session = session_file[sid]

    return (cookie, session, session_file)

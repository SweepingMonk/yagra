#!/usr/bin/env python
import cgi, cgitb

cgitb.enable()

print "Content-Type: text/html"
print

cgi.print_environ()

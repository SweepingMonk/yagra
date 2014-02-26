#!/usr/bin/env python
#_*_coding:utf-8_*_
import cgitb
import helper

cgitb.enable()

def get(http_request, http_response):
    """
    http get function
    """
    request_data = http_request.parameters
    email_digest = request_data.getvalue("uid")
    if email_digest is None or email_digest == "":
        print "Content-Type: text/plain"
        print
        print "Error!"
    else:
        current_user = helper.User()
        current_user.email_digest = email_digest
        image_path = "../userimage/avatar.jpg"
        if not current_user.load_by_email_digest():
            print "Content-Type: text/plain"
            print
            print "用户不存在!"
            return
        elif current_user.default_image is not None:
            image_path = "../userimage/{user.id_}/{user.default_image}"\
                    .format(user=current_user)
        http_response.header["Content-Dispostion"] = 'attachment; filename="{0}"'\
                .format(image_path[image_path.rindex("/")+1:])
        http_response.header["Content-Type"] = "image/jpeg"
        with open(image_path, "rb") as image_fp:
            buff = image_fp.read()
            http_response.send_binary(buff)

if __name__ == '__main__':
    if helper.http_request.http_method == "GET":
        get(helper.http_request, helper.http_response)
    elif helper.http_request.http_method == "POST":
        get(helper.http_request, helper.http_response)

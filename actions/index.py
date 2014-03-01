#!/usr/bin/env python
#_*_coding:utf-8_*_
import cgitb
import os
import helper

cgitb.enable()

def get(http_request, http_response):
    """
    http get function
    """
    session = http_request.get_session()
    if "user" not in session:
        http_response.send_redirect("login")
    else:
        current_user = session["user"]
        images = os.listdir("../userimage/{0}".format(current_user.id_))
        #image html template
        defaultimage_template = '<div class="image default"><img src="{0}"></div>'
        normalimage_template = '<div class="image"><img src="{0}"></div>'

        image_path = "/userimage/avatar.jpg"
        image_list = ""
        if current_user.default_image is not None:
            image_path = "/userimage/{user.id_}/{user.default_image}"\
                    .format(user=current_user)
            for image in images:
                path = "/userimage/{0}/{1}".format(current_user.id_, image)
                if current_user.default_image == image:
                    image_list = "".join([
                        image_list,
                        defaultimage_template.format(path)
                        ])
                else:
                    image_list = "".join([
                        image_list,
                        normalimage_template.format(path)
                        ])

        http_request.close_session_file()
        http_response.send_html(
                "index.html",
                image_path=image_path,
                email=current_user.email,
                email_digest=current_user.email_digest,
                image_list=image_list)

if __name__ == '__main__':
    if helper.http_request.http_method == "GET":
        get(helper.http_request, helper.http_response)
    elif helper.http_request.http_method == "POST":
        get(helper.http_request, helper.http_response)

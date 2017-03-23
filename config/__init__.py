#!/usr/bin/env python
#
# Copyright 2015 Alec Golibroda
#

""" Config."""

# from __future__ import absolute_import, division, print_function, with_statement


from tornado.options import define, options, parse_config_file
# options.logging = debug #None


#
define("Project_Name", default= 'TorWiki', help="Project name")

define("salt", default= '$2b$12$.b9454ab5a22859b68bb48a65ed3be7ab208c', help="Main salt")
define("cookie_secret", default= '64d1c3defc5f9e829010881cfae22db38732', help="Main cookie_secret")

########################################################################
define("postgreHost", default="localhost", help="postgreHost")
define("postgrePort", default="5432", help="postgrePort")

define("postgreBase", default="py_wiki", help="postgreBase")

define("postgreUser", default="postgres", help="postgreUser")
define("postgrePwd", default="123", help="postgrePwd")
########################################################################


define("main_port", default="8888", help="Main port 8888")
define("main_title", default="Main WIKI Title", help="Main Wiki Title ")


define("uploud_path", default="static/filestorage/", help="Path to upload")
define("to_out_path", default="filestorage/", help="Path to upload")

define("adminPath", default=r"/admin", help="Path to Admin Area")
define("adminTplPath", default=r"admin/", help="Path to Admin Area")

define("tmpTplPath", default=r"tmp", help="Path to user`s Template Area")
define("tplExtension", default=r".html", help="Template file Extension")


define("list_categofy_id", default=1, help="Information Page Category")

define("info_page_categofy_id", default=3, help="Information Page Category")
define("tpl_categofy_id", default=4, help="Template Page Category")

define("main_info_template", default=5, help="Main tmplate of inforation page")
define("main_page_id", default=6, help="Id of Main User Page")




# parse_config_file("./config/base.conf")
parse_config_file("./config/main.conf")



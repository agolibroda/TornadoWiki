#!/usr/bin/env python
#
# Copyright 2015 Alec Golibroda
#

""" Config."""

# from __future__ import absolute_import, division, print_function, with_statement


from tornado.options import define, options, parse_config_file
# options.logging = debug #None


define("salt", default= '$2b$12$.b9454ab5a22859b68bb48a65ed3be7ab208c', help="Main salt")
define("cookie_secret", default= '64d1c3defc5f9e829010881cfae22db38732', help="Main cookie_secret")


# define("mysql_host", default="127.0.0.1:3306", help="Main user DB")
define("mysql_host", default="localhost", help="Main host DB")
define("mysql_port", default="3306", help="Main port DB")
# define("memcache_hosts", default="127.0.0.1:11011", multiple=True, help="Main user memcache servers")

define("mysql_user", default="root", help="User Name")
define("mysql_password", default="", help="User PAss")
define("mysql_db", default="wiki", help="Work DB Name")
define("mysql_charset", default="utf8mb4", help="CharSet")


define("main_port", default="8888", help="Main port 8888")
define("main_title", default="Main WIKI Title", help="Main Wiki Title ")


define("uploud_path", default="static/filestorage/", help="Path to upload")
define("to_out_path", default="filestorage/", help="Path to upload")

define("adminPath", default=r"/admin", help="Path to Apmen Area")
define("adminTplPath", default=r"admin/", help="Path to Apmen Area")

define("main_page_id", default=5, help="Id of Main User Page")
define("info_page_categofy_id", default=4, help="Information Page Category")

define("list_categofy_id", default=1, help="Information Page Category")

define("list_tpl_categofy_id", default=3, help="Template Page Category")
define("main_info_template", default=6, help="Main tmplate of inforation page")




# parse_config_file("./config/base.conf")
parse_config_file("./config/main.conf")



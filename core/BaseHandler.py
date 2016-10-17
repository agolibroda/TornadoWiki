#!/usr/bin/env python
#
# Copyright 2015 Alec Golibroda


#  Впринцепе, Это "тулБокс" - ящик с инструментами просто пользователя 
# надо сюда добавить 
# список ПОльзователей
# список Групп 


import bcrypt
import concurrent.futures

import os.path
import re
import subprocess
# import torndb
import tornado.escape
from tornado import gen
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import unicodedata

import logging
import json

import config

import core.models

from core.models.user import User
# from core.models.article import Article
# from core.models.article import Revision
# from core.models.file import File
# from core.models.template import Template
# 
# from core.control.article import ControlArticle 



# A thread pool to be used for password hashing with bcrypt.
executor = concurrent.futures.ThreadPoolExecutor(2)


class BaseHandler(tornado.web.RequestHandler):
#     @property
#     def db(self):
#         return self.application.db

    def get_current_user(self):
        try:
            user_id = int(self.get_secure_cookie("wiki_user"))
        except:
            user_id = 0
        logging.info('BaseHandler:: get_current_user:: user_id '+ str(user_id))
        if not user_id: return None
        user = User()
        user = user.get(user_id)
#         logging.info('BaseHandler:: get_current_user:: user '+ str(user))

        return user

    def any_author_exists(self):
        return bool(self.get_current_user())




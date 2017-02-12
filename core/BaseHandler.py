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

from core.models.author import Author
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
        self.author = Author()
        try:
            author_id = int(self.get_secure_cookie("wiki_author"))
            logging.info('BaseHandler:: get_current_user:: author_id '+ str(author_id))
            if not author_id or author_id == 0: return None
            if self.author.author_id == 0:
                self.author = self.author.get(author_id)
#         logging.info('BaseHandler:: get_current_user:: author '+ str(author))

        except Exception as e:
            logging.info('BaseHandler:: get_current_user:: Have Error!!! '+ str(e))
            return None
#             author_id = 0

        return self.author

    def any_author_exists(self):
        return bool(self.get_current_user())




#!/usr/bin/env python
#
# Copyright 2015 Alec Golibroda


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
from core.models.article import Article
from core.models.article import Revision
from core.models.file import File

from core.control.article import ControlArticle 



# A thread pool to be used for password hashing with bcrypt.
executor = concurrent.futures.ThreadPoolExecutor(2)


class RestHandler(tornado.web.RequestHandler):
#     @property
#     def db(self):
#         return self.application.db

    def get_current_user(self):
        try:
            user_id = int(self.get_secure_cookie("wiki_user"))
        except:
            user_id = 0
        logging.info('RestHandler:: get_current_user:: user_id '+ str(user_id))
        if not user_id: return None
        user = User()
        user = user.get(user_id)
        logging.info('RestHandler:: get_current_user:: user '+ str(user))

        return user

    def any_author_exists(self):
        return bool(self.get_current_user())



class RestMinHandler(RestHandler):
    """
    тут будем разбирать ситуЁвину - что и куда делать... 
    
    """

    @gen.coroutine
    def get(self, commandName, currentCategory):

        logging.info('RestHandler:: commandName '+ str(commandName))
        logging.info('RestHandler:: currentCategory '+ str(currentCategory))
        
        if int(currentCategory) == 0:
            currentCategory = config.options.info_page_categofy_id
        
        if commandName == 'getArticleCategoryList':

            artControl = ControlArticle()
            articles = yield executor.submit( artControl.getListArticles, config.options.list_categofy_id)
            logging.info('RestMinHandler:: commandName:: articles '+ str(articles))
            # получить список данных
            
            self.render("rest/ctegory_list.html", dataList=articles, selected=int(currentCategory))




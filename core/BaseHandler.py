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

from core.models.author     import Author
from core.models.group      import Group

# from core.models.article import Article
# from core.models.article import Revision
# from core.models.file import File
# from core.models.template import Template
# 
# from core.control.article import ControlArticle 



# A thread pool to be used for password hashing with bcrypt.
executor = concurrent.futures.ThreadPoolExecutor(2)


class SingletonDecorator:
    def __init__(self,klass):
        self.klass = klass
        self.instance = None
    def __call__(self,*args,**kwds):
        if self.instance == None:
            self.instance = self.klass(*args,**kwds)
        return self.instance

# class Top: pass
# _Top = SingletonDecorator(Top)
# q=_Top()
# q.val = 'qqqqqqqq'
# print(q.val)


class BaseHandler(tornado.web.RequestHandler):
#     @property
#     def db(self):
#         return self.application.db
#     x = OnlyOne('sausage')

#     _Author = SingletonDecorator(Author)
    
    def get_current_user(self):
        """
        Это Стандартный торнадовский функций, про получение данных о пользователе
        
        """
        self.author = SingletonDecorator(Author)()
        try:
            author_id = int(self.get_secure_cookie("wiki_author"))
#             logging.info('BaseHandler:: get_current_user:: author_id '+ str(author_id))
            if not author_id or author_id == 0: return None
#             logging.info('BaseHandler:: get_current_user:: self.author '+ str(self.author))
            if self.author.author_id == 0:
                self.author = self.author.get(author_id)
#                 self.author =  yield executor.submit( self.author.get, author_id)
            logging.info('BaseHandler:: get_current_user:: self.author '+ str(self.author))

        except Exception as e:
            logging.info('BaseHandler:: get_current_user:: Have Error!!! '+ str(e))
            return None
#             author_id = 0

        return self.author

    def any_author_exists(self):
        return bool(self.get_current_user())




class AuthorsHandler(BaseHandler):
    """
     все тоже самое, что и в "BaseHandler", только 
     добавлю загрузку списка персональных групп для заполнения меню
       
     
    """

    class TemplateParams:
        pass

#     @tornado.web.authenticated
    def __init__(self, application, request, **kwargs):
        """
        вот тут и загрузим список групп пользователя.
          
        """
        super(AuthorsHandler, self).__init__(application, request, **kwargs)
        self.templateParams = SingletonDecorator(self.TemplateParams)()
        
    def makeTplParametr (self):
        """
        для работы с формами, туда надо передать некоорое количество данных. 
        все эти данные надо собрать в объкт (одиночку) TemplateParams
        и пользоваться его данными
        
        """
        
        if hasattr(self.templateParams, 'autorGroupList'): 
            groupModel = Group()
            self.templateParams.autorGroupList = yield executor.submit( groupModel.grouplistForAutor, self.author.author_id )
        

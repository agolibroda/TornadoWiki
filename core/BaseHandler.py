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

import pickle

import config


from core.Helpers           import *

from core.models.group      import Group

import core.models

from core.models.author     import Author

# from core.models.article import Article
# from core.models.article import Revision
# from core.models.file import File
# from core.models.template import Template
# 
# from core.control.article import ControlArticle 



# A thread pool to be used for password hashing with bcrypt.
executor = concurrent.futures.ThreadPoolExecutor(2)


@singleton
class TemplateParams:
    """
     место хранения всех параметров, которые надо передавать в шаблон        
     
    """
#     @gen.coroutine
    def make (self, author):
        """
        для работы с формами, туда надо передать некоорое количество данных. 
        все эти данные надо собрать в объкт (одиночку) TemplateParams
        и пользоваться его данными
          
        """
#         logging.info( ' makeTplParametr:: self = ' + str(self))
#         if not hasattr(self, 'autorGroupList'): 

#         logging.info( ' makeTplParametr:: get autorGroupList NOW! = ')
        self.author = author
        groupModel = Group()
#         self.autorGroupList = yield executor.submit( groupModel.grouplistForAutor, self.author.author_id )
        self.autorGroupList = groupModel.grouplistForAutor( self.author.author_id )
         
#         logging.info (' makeTplParametr:: self = ' + toStr( self))
     

@singleton
class SingletonAuthor(Author):
    pass

class BaseHandler(tornado.web.RequestHandler):
#     @property
#     def db(self):
#         return self.application.db
#     x = OnlyOne('sausage')

#     @singleton
#     class __Autor:
#         def __init__(self):
#             self.locAuthor = self.__Autor()
        
#     @gen.coroutine
    def get_current_user(self):
        """
        Это Стандартный торнадовский функций, про получение данных о пользователе
        
        """
# походу, это какая  - то не правильная версия одиночки!!!!
# надо проверить - то, что лежит в модеи!!!!

        self.author = SingletonAuthor()
        try:
            author_id = int(self.get_secure_cookie("wiki_author"))
#             logging.info('BaseHandler:: get_current_user:: get_secure_cookie author_id '+ str(author_id))
            if not author_id or author_id == 0: return None
#             logging.info('BaseHandler:: get_current_user:: 11 self.author '+ str(self.author))
            if self.author.author_id == 0:
                self.author = self.author.get(author_id)
#                 self.author =  yield executor.submit( self.author.get, author_id)
#             logging.info('BaseHandler:: get_current_user:: 22 self.author '+ str(self.author))

        except Exception as e:
            logging.info('BaseHandler:: get_current_user:: Have Error!!! '+ str(e))
            return None
#             author_id = 0

        return self.author

    def any_author_exists(self):
        return bool(self.get_current_user())





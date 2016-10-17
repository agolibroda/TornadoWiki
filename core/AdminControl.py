#!/usr/bin/env python
#
# Copyright 2015 Alec Golibroda

# 
# 
# AdminHandler.py
# 
#  чем по - идее, имею дело? 
#  Админ - это просмотр списка 
#  Впринцепе, Это "тулБокс" - ящик с инструментами СуперАдмина

# надо сюда добавить 
# список ПОльзователей
# список Групп 

#  - пользователей
#  - материалов 
#  - редактирование пользователей
#  - работа с правами
#  
#  что еще? пока не знаю.
 

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

from core.models.user       import User
from core.models.article    import Article
from core.models.article    import Revision
from core.models.file       import File

from core.control.article   import ControlArticle 

from core.models.template   import Template

from core.BaseHandler import *


# A thread pool to be used for password hashing with bcrypt.
executor = concurrent.futures.ThreadPoolExecutor(2)


class AdminHomeHandler(BaseHandler):
    """
    по - идее, это админка "как таковая" 
    то есть то, сто будет содержать список людей, список статей, список групп
    что - то типа "фара" на три колонки.... 
    и с возможностью прыгать по ним - и редактировать... 
    или куда.... 
    то чисто показуха 
    и перевод вопроса в другие специализированные инструменты
    
    Кстати, нечто подобное будет и для пользователя.
    
    """
    
#     def initialize(self, flag):
#         logging.info( 'AdminHomeHandler:: __init__:: flag = ' + str(flag))
#         self.flag = flag

#     def __init__(self, flag):
#         """
#         """
#         logging.info( 'AdminHomeHandler:: __init__:: flag = ' + str(flag))
         
         
    @tornado.web.authenticated
    @gen.coroutine
    def get(self):
        """
        и шаблон должен быть что - то типа "АдминДома" -) 
        и набирать его... 
        или, набирать тот шаблон через вызовы реста? 
        ну да, тут  - просто шаблон (и проверку рав - а можно ли какретному пользователю Админить, и тогда  ))
        или 403  - нету правов, или шаблон "автозаполнялку..." 

        """
        try:
            logging.info( 'AdminHomeHandler:: get ')
            artControl = ControlArticle()
            articles = yield executor.submit( artControl.getListArticles )
    
    
            self.render(config.options.adminTplPath+"admin_home.html", articles=articles, tplCategory=config.options.tpl_categofy_id )
        except Exception as e:
            logging.info( 'Save:: Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.render('error.html', error=error)





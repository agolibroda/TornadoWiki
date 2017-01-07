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

from core.models.author     import Author
from core.models.article    import Article
from core.models.file       import File

from core.models.group      import Gpoup

from core.helpers.article import HelperArticle 


from core.models.template   import Template

from core.BaseHandler import *
from core.WikiException import *



# A thread pool to be used for password hashing with bcrypt.
executor = concurrent.futures.ThreadPoolExecutor(2)


class PersonalDeskTop(BaseHandler):
    """
    Персональнвый рабочий стол пользователя.
    
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
#             logging.info( 'AdminHomeHandler:: get ')
#             artControl = ControlArticle()
#             articles = yield executor.submit( artControl.getListArticles )
    
            author = self.get_current_user() # current_user
            logging.info( 'PersonalDeskTop:: author ' + str(author))
    
#             self.render("personal_dt.html", page_name= 'Рабочий стол ' + " пользователь??? " , tplCategory=config.options.tpl_categofy_id )
            self.render("personal_dt.html", page_name= 'Рабочий стол ' + author.author_name, link='personal_desk_top')

        except Exception as e:
            logging.info( 'PersonalDeskTop get:: Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.render('error.html', error=error, page_name= 'Рабочий стол ', link='personal_desk_top')


class GroupDeskTop(BaseHandler):
    """
    Персональнвый рабочий стол уастника группы.
    
    """
    @tornado.web.authenticated
    @gen.coroutine
    def get(self, group_id=0):
        """
        и шаблон должен быть что - то типа "АдминДома" -) 
        и набирать его... 
        или, набирать тот шаблон через вызовы реста? 
        ну да, тут  - просто шаблон (и проверку рав - а можно ли какретному пользователю Админить, и тогда  ))
        или 403  - нету правов, или шаблон "автозаполнялку..." 

        """
        try:
            logging.info( 'GroupDeskTop:: get group_id = ' + str(group_id))

            curentAuthor = yield executor.submit(self.get_current_user ) #self.get_current_user ()
            if not curentAuthor.author_id: return None
            
            groupModel = Gpoup()
    

            if group_id==0:
                groupName = ''
                groupData = groupModel
            else:
                groupData = yield executor.submit( groupModel.get, group_id )
                logging.info( 'GroupDeskTop:: get groupData = ' + str(groupData))
                groupName = groupData.group_title    
    
            self.render("group_dt.html", group=groupData, page_name= groupName, link='group_dt')
        except Exception as e:
            logging.info( 'GroupDeskTop Get:: Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.render('error.html', error=error)


    @tornado.web.authenticated
    @gen.coroutine
    def post(self, group_id=0):
        try:
            logging.info( 'GroupDeskTop:: post group_id = ' + str(group_id))
            curentAuthor = yield executor.submit(self.get_current_user ) #self.get_current_user ()
            if not curentAuthor.author_id: return None
    
            groupModel = Gpoup()
    
            groupModel.group_id = int(self.get_argument("id", 0))
            groupModel.group_title = self.get_argument("title")
            groupModel.group_annotation = self.get_argument("annotation")
            groupModel.group_status = self.get_argument("status", 'pbl')                                
            
            logging.info( 'GroupDeskTop:: Before Save! groupModel = ' + str(groupModel))
            
            rez = yield executor.submit( groupModel.save, curentAuthor.author_id )
    #         logging.info( 'GroupDeskTop:: AFTER Save! groupModel = ' + str(groupModel))
            
            self.redirect("/group_desk_top/" + str(groupModel.group_id))
        except Exception as e:
            logging.info( 'GroupDeskTop POST!!! (Save):: Exception as et = ' + str(e))
#             error = Error ('500', 'что - то пошло не так :-( ')
#             self.render('error.html', error=error, link='/compose', page_name='')
            pageName = 'Редактирование ' + groupModel.group_title
            self.render("group_dt.html", group=group, page_name= pageName, link='group_dt')



class GroupAdmDeskTop(BaseHandler):
    """
    Персональнвый рабочий стол админа группы.
    
    """
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
#             logging.info( 'AdminHomeHandler:: get ')
#             artControl = ControlArticle()
#             articles = yield executor.submit( artControl.getListArticles )
    
    
            self.render(config.options.adminTplPath+"admin_home.html", articles=articles, tplCategory=config.options.tpl_categofy_id )
        except Exception as e:
            logging.info( 'Save:: Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.render('error.html', error=error)



class SysAdmDeskTop(BaseHandler):
    """
    Персональнвый рабочий стол админа системы.
    
    """
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
#             artControl = ControlArticle()
#             articles = yield executor.submit( artControl.getListArticles )
    
    
            self.render(config.options.adminTplPath+"admin_home.html", articles=articles, tplCategory=config.options.tpl_categofy_id )
        except Exception as e:
            logging.info( 'Save:: Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.render('error.html', error=error)


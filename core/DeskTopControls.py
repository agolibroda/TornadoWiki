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

import pickle

import config

# import core.Helpers
from core.Helpers           import *
# from core.Helpers           import SingletonDecorator

import core.models
from core.models.author     import Author
from core.models.article    import Article
from core.models.file       import File

from core.models.group      import Group

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
            author = self.get_current_user() 
    
            tplControl = TemplateParams()
            tplControl.make(author)

            tplControl.page_name = 'Рабочий стол ' + author.author_name
            tplControl.link='personal_desk_top'

            artHelper = HelperArticle()
            tplControl.personalArticlesList = yield executor.submit( artHelper.getListArticlesByAutorId, author.author_id, author.author_id )
            groupModel = Group()
            tplControl.autorGroupList = yield executor.submit( groupModel.grouplistForAutor, author.author_id )
            artHelper = HelperArticle()
            articles = yield executor.submit( artHelper.getListArticlesByAutorId, author.author_id )
            tplControl.articlesList = articles
            articlesAll = yield executor.submit( artHelper.getListArticlesAll, author.author_id )
            tplControl.allArticlesList = articlesAll
            groupList = yield executor.submit( groupModel.list )
            tplControl.allGroupsList = groupList
            authorModel = Author()
            authorList = yield executor.submit( authorModel.list )
            tplControl.allAuthorsList = authorList

            self.render("personal_dt.html", parameters= tplControl ) 

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

            author = self.get_current_user() 

            if not author.author_id: return None

            groupModel = Group()
    
            if group_id==0:
                groupName = 'Create New Group'
                groupData = groupModel
            else:
                groupData = yield executor.submit( groupModel.get, group_id )
                groupName = groupData.group_title 

            logging.info( 'GroupDeskTop Get:: 1 = ' + str(True))
            tplControl = TemplateParams()
            tplControl.make(author)
            tplControl.page_name = groupName 
            tplControl.groupData = groupData

            articles = yield executor.submit( groupModel.getGroupArticleList, group_id )
            tplControl.articlesList = articles 
            logging.info( 'GroupDeskTop Get:: 2 = ' + str(True))
            members = yield executor.submit( groupModel.getGroupMembersleList, group_id )
            tplControl.groupMembersList = members 
            logging.info( 'GroupDeskTop Get:: 3 = ' + str(True))

            if int(group_id) == 0:
                tplControl.link = 'group_desk_top'
            else:
                tplControl.link='group_desk_top/' + str(group_id)   

            logging.info( 'GroupDeskTop Get:: 4 = ' + str(True))

            self.render("group_dt.html", parameters= tplControl)
        except Exception as e:
            logging.info( 'GroupDeskTop Get:: Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.render('error.html', error=error)


    @tornado.web.authenticated
    @gen.coroutine
    def post(self, group_id=0):
        try:
            author = self.get_current_user() 
    
            groupModel = Group()
    
            groupModel.group_id = int(self.get_argument("id", 0))
            groupModel.group_title = self.get_argument("title")
            groupModel.group_annotation = self.get_argument("annotation")
            groupModel.group_status = self.get_argument("status", 'pbl')                                
            
            rez = yield executor.submit( groupModel.save, author.author_id )
            
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
            self.render(config.options.adminTplPath+"admin_home.html", articles=articles, tplCategory=config.options.tpl_categofy_id )
        except Exception as e:
            logging.info( 'Save:: Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.render('error.html', error=error)


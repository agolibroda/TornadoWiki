#!/usr/bin/env python
#
# Copyright 2015 Alec Golibroda

# RestControl.py

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
from core.models.article import Article
from core.models.file import File

from core.helpers.article import HelperArticle 

from core.models.group      import Gpoup


from core.BaseHandler import *


# A thread pool to be used for password hashing with bcrypt.
executor = concurrent.futures.ThreadPoolExecutor(2)



class RestMinHandler(BaseHandler):
    """
    тут будем разбирать ситуЁвину - что и куда делать... 
    
    """

    @gen.coroutine
    def get(self, commandName, curentParameter, label=''):

        logging.info('RestMinHandler:: commandName '+ str(commandName))
        logging.info('RestMinHandler:: curentParameter '+ str(curentParameter))

        link=self.get_argument('link', '')
        logging.info('RestMinHandler:: link = '+ str(link))

        
        curentAuthor = yield executor.submit(self.get_current_user ) #self.get_current_user ()
        
        
        if commandName == 'getArticleTemplateList':
            
            label=self.get_argument('label')
            selector=self.get_argument('selector')
            
            logging.info('RestMinHandler:: curentParameter::'+ str(curentParameter))
            logging.info('RestMinHandler:: label '+ str(label))
            logging.info('RestMinHandler:: selector '+ str(selector))

            if int(curentParameter) == 0:
                curentParameter = config.options.main_info_template
                articles = [Article(0, 'Выберите значение ')]
            else:
                articles = []
            
            artHelper = HelperArticle()
            articles += yield executor.submit(artHelper.getListArticles, config.options.tpl_categofy_id)
            logging.info('RestMinHandler:: commandName:: getArticleTemplateList '+ str(articles))
            # получить список данных

            self.render("rest/templates_list.html", dataList=articles, itemName=selector, selected=int(curentParameter), label=label)

        if commandName == 'getArticleCategoryList':
            try:
                label=self.get_argument('label')
                selector=self.get_argument('selector')
                
                logging.info('RestMinHandler:: curentParameter::'+ str(curentParameter))
                logging.info('RestMinHandler:: label '+ str(label))
    
                if int(curentParameter) == 0:
                    curentParameter = config.options.main_info_template
                    articles = [Article(0, 'Выберите значение ')]
                else:
                    articles = []
                
                artHelper = HelperArticle()
                articles += yield executor.submit(artHelper.getListArticles, config.options.list_categofy_id)
                logging.info('RestMinHandler:: commandName:: getArticleTemplateList '+ str(articles))
                # получить список данных
    
                self.render("rest/templates_list.html", dataList=articles, itemName=selector, selected=int(curentParameter), label=label)
            except Exception as e:
                logging.info( 'getArticleCategoryList:: Exception as et = ' + str(e))
                error = Error ('500', 'что - то пошло не так :-( ')
                self.render('table_error.html', error=error)


        if commandName == 'getPersonalArticlesList': 
            try:
#                 curentAuthor = yield executor.submit(self.get_current_user ) #self.get_current_user ()
# #                 curentAuthor = self.get_current_user ()
                logging.info( 'getPersonalArticlesList:: get curentAuthor = ' + str(curentAuthor))
                
                artHelper = HelperArticle()
                articles = yield executor.submit( artHelper.getListArticlesByAutorId, curentAuthor.author_id )
                self.render("rest/articles_list.html", articles=articles)
            except Exception as e:
                logging.info( 'getPersonalArticlesList:: Exception as et = ' + str(e))
                error = Error ('500', 'что - то пошло не так :-( ')
                self.render('table_error.html', error=error)


        # получить список всех статей, размещнных в группе
        if commandName == 'getGroupArticleList': 
            try:
                groupModel = Gpoup()
                articles = yield executor.submit( groupModel.getGroupArticleList, curentParameter )
                self.render("rest/articles_group_list.html", articles=articles, group=curentParameter )
            except Exception as e:
                logging.info( 'getGroupArticleList:: Exception as et = ' + str(e))
                error = Error ('500', 'что - то пошло не так :-( ')
                self.render('table_error.html', error=error)

        # получить список всех участников  группы
        if commandName == 'getGroupMembersleList': 
            try:
                groupModel = Gpoup()
                members = yield executor.submit( groupModel.getGroupMembersleList, curentParameter )
                self.render("rest/members_list.html", members=members)
            except Exception as e:
                logging.info( 'getGroupMembersleList:: Exception as et = ' + str(e))
                error = Error ('500', 'что - то пошло не так :-( ')
                self.render('rest/rest_error.html', error=error)


        # получить список всех групп, в которых мемберит конкретный ползователь (А-М - важно :-) )
        if commandName == 'getPersonalGroupList': 
            try:
#                 curentAuthor = yield executor.submit(self.get_current_user ) #self.get_current_user ()
                if not curentAuthor.author_id: return None
                logging.info( 'getPersonalGroupList:: get curentAuthor = ' + str(curentAuthor))
                groupModel = Gpoup()
                groupList = yield executor.submit( groupModel.grouplistForAutor, curentAuthor.author_id )
                self.render("rest/personal_group_list.html", groupList=groupList, link=link)
            except Exception as e:
                logging.info( 'getPersonalGroupList:: Exception as et = ' + str(e))
                error = Error ('500', 'что - то пошло не так :-( ')
                self.render('rest/rest_error.html', error=error)


#             membersGroupList = yield executor.submit( groupModel.get, curentAuthor.author_id )
#             groupModel = Gpoup()


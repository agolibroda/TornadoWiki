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

        logging.info('BaseHandler:: commandName '+ str(commandName))
        logging.info('BaseHandler:: curentParameter '+ str(curentParameter))
        
        curentAuthor = yield executor.submit(self.get_current_user ) #self.get_current_user ()
        
        
#         if commandName == 'getArticleCategoryList':
# 
#             if int(curentParameter) == 0:
#                 curentParameter = config.options.info_page_categofy_id
#             
#             articles = [Article(0, 'Выберите значение ')]
#             artHelper = HelperArticle()
#             articles += yield executor.submit( artHelper.getListArticles, config.options.list_categofy_id)
#             logging.info('RestMinHandler:: commandName:: getArticleCategoryList '+ str(articles))
#             # получить список данных
#             
#             self.render("rest/ctegory_list.html", dataList=articles,  itemName="category_article_id", selected=int(curentParameter))


        if commandName == 'getArticleTemplateList':
            
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
            articles += yield executor.submit(artHelper.getListArticles, config.options.tpl_categofy_id)
            logging.info('RestMinHandler:: commandName:: getArticleTemplateList '+ str(articles))
            # получить список данных

            self.render("rest/templates_list.html", dataList=articles, itemName=selector, selected=int(curentParameter), label=label)

        if commandName == 'getArticleCategoryList':
            
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


        if commandName == 'getPersonalArticlesList': 
            try:
                curentAuthor = yield executor.submit(self.get_current_user ) #self.get_current_user ()
                logging.info( 'getPersonalArticlesList:: get curentAuthor = ' + str(curentAuthor))
                
                artHelper = HelperArticle()
                articles = yield executor.submit( artHelper.getListArticlesByAutorId, curentAuthor.author_id )
#                 if not articles:
#                     self.redirect("/compose")
#                     return
                self.render("rest/articles_list.html", articles=articles)
            except Exception as e:
                logging.info( 'Load:: Exception as et = ' + str(e))
                error = Error ('500', 'что - то пошло не так :-( ')
                self.render('table_error.html', error=error)


        # получить список всех статей, размещнных в группе
        if commandName == 'getGroupArticleList': 
#             if not curentAuthor.author_id: return None
            logging.info( 'getGroupArticleList:: get curentAuthor = ' + str(curentAuthor))
            logging.info('getGroupArticleList:: curentParameter '+ str(curentParameter))

        # получить список всех участников  группы
        if commandName == 'getGroupMembersleList': 
#             if not curentAuthor.author_id: return None
            logging.info( 'getGroupMembersleList:: get curentAuthor = ' + str(curentAuthor))
            logging.info('getGroupMembersleList:: curentParameter '+ str(curentParameter))


        # получить список всех групп, в которых мемберит конкретный ползователь (А-М - важно :-) )
        if commandName == 'getPersonalGroupList': 
            if not curentAuthor.author_id: return None
            logging.info( 'getPersonalGroupList:: get curentAuthor = ' + str(curentAuthor))

            groupModel = Gpoup()
            
            groupList = yield executor.submit( groupModel.grouplistForAutor, curentAuthor.author_id )

            self.render("rest/personal_group_list.html", groupList=groupList)


#             membersGroupList = yield executor.submit( groupModel.get, curentAuthor.author_id )
#             groupModel = Gpoup()


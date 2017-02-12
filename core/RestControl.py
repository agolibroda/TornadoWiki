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

from core.models.group      import Group


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

        
        self.curentAuthor = yield executor.submit(self.get_current_user ) #self.get_current_user ()
        logging.info( 'getPersonalArticlesList:: get self.curentAuthor = ' + str(self.curentAuthor))
        
        
        try:
            if commandName == 'getArticleTemplateList':
                
                label=self.get_argument('label')
                selector=self.get_argument('selector')
                
                if int(curentParameter) == 0:
                    curentParameter = config.options.main_info_template
                    articles = [Article(0, 'Выберите значение ')]
                else:
                    articles = []
                
                artHelper = HelperArticle()
                articles += yield executor.submit(artHelper.getListArticles, config.options.tpl_categofy_id)
    
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
    
                self.render("rest/templates_list.html", dataList=articles, itemName=selector, selected=int(curentParameter), label=label)


            if commandName == 'getPersonalArticlesList': 
                artHelper = HelperArticle()
                articles = yield executor.submit( artHelper.getListArticlesByAutorId, self.curentAuthor.author_id )
                self.render("rest/articles_list.html", articles=articles)


            # получить список всех статей, размещнных в группе
            if commandName == 'getGroupArticleList': 
                groupModel = Group()
                articles = yield executor.submit( groupModel.getGroupArticleList, curentParameter )
                logging.info( 'getGroupArticleList:: get articles = ' + str(articles))

                self.render("rest/articles_group_list.html", articles=articles, group=curentParameter )

            # получить список всех участников  группы
            if commandName == 'getGroupMembersleList': 
                groupModel = Group()
                members = yield executor.submit( groupModel.getGroupMembersleList, curentParameter )
                self.render("rest/members_list.html", members=members)

            # получить список всех групп, в которых мемберит конкретный ползователь (А-М - важно :-) )
            if commandName == 'getPersonalGroupList': 
#                 curentAuthor = yield executor.submit(self.get_current_user ) #self.get_current_user ()
                if not self.curentAuthor.author_id: return None
                groupModel = Group()
                groupList = yield executor.submit( groupModel.grouplistForAutor, self.curentAuthor.author_id )
                self.render("rest/personal_group_list.html", groupList=groupList, link=link)

            #  получить список всех групп, которые есть в системе. и сделать из них табличку.
            if commandName == 'getAllGroupList': 
#                 curentAuthor = yield executor.submit(self.get_current_user ) #self.get_current_user ()
#                 if not self.curentAuthor.author_id: return None
                groupModel = Group()
                groupList = yield executor.submit( groupModel.list )
                self.render("rest/all_group_list.html", groupList=groupList, link=link)

            #  получить список пользователей
            if commandName == 'getAllAuthorList': 
                logging.info( 'getAllauthorList:: start!!!! ' )
                authorModel = Author()
                authorList = yield executor.submit( authorModel.list )
                
                logging.info( 'getAllauthorList:: get authorList = ' + str(authorList))
                
                self.render("rest/all_author_list.html", authorList=authorList, link=link)





        except Exception as e:
            logging.info( 'commandName:: '+ str(commandName)+' Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.render('table_error.html', error=error)



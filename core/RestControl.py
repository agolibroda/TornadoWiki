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
from core.models.article import Revision
from core.models.file import File

from core.helpers.article import HelperArticle 


from core.BaseHandler import *


# A thread pool to be used for password hashing with bcrypt.
executor = concurrent.futures.ThreadPoolExecutor(2)



class RestMinHandler(BaseHandler):
    """
    тут будем разбирать ситуЁвину - что и куда делать... 
    
    """

    @gen.coroutine
    def get(self, commandName, curentParameter):

        logging.info('BaseHandler:: commandName '+ str(commandName))
        logging.info('BaseHandler:: curentParameter '+ str(curentParameter))
        
        
        if commandName == 'getArticleCategoryList':

            if int(curentParameter) == 0:
                curentParameter = config.options.info_page_categofy_id
            
            articles = [Article(0, 'Выберите значение ')]
            artHelper = HelperArticle()
            articles += yield executor.submit( artHelper.getListArticles, config.options.list_categofy_id)
            logging.info('RestMinHandler:: commandName:: getArticleCategoryList '+ str(articles))
            # получить список данных
            
            self.render("rest/ctegory_list.html", dataList=articles,  itemName="category_article_id", selected=int(curentParameter))


        if commandName == 'getArticleTemplateList':

            if int(curentParameter) == 0:
                curentParameter = config.options.main_info_template

            articles = [Article(0, 'Выберите значение ')]
            artHelper = HelperArticle()
            articles += yield executor.submit( artHelper.getListArticles, config.options.tpl_categofy_id)
            logging.info('RestMinHandler:: commandName:: getArticleTemplateList '+ str(articles))
            # получить список данных

            self.render("rest/ctegory_list.html", dataList=articles, itemName="template_id", selected=int(curentParameter))


        if commandName == 'getPersonalArticlesList': 
            try:
                curentAuthor = yield executor.submit(self.get_current_user ) #self.get_current_user ()
                logging.info( 'getPersonalArticlesList:: get curentAuthor = ' + str(curentAuthor))
                
                artHelper = HelperArticle()
                articles = yield executor.submit( artHelper.getListArticlesByAutorId, curentAuthor.author_id )
                if not articles:
                    self.redirect("/compose")
                    return
                self.render("rest/articles_list.html", articles=articles)
            except Exception as e:
                logging.info( 'Load:: Exception as et = ' + str(e))
                error = Error ('500', 'что - то пошло не так :-( ')
                self.render('table_error.html', error=error)




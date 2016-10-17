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

from core.models.user import User
from core.models.article import Article
from core.models.article import Revision
from core.models.file import File

from core.control.article import ControlArticle 

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
            artControl = ControlArticle()
            articles += yield executor.submit( artControl.getListArticles, config.options.list_categofy_id)
            logging.info('RestMinHandler:: commandName:: getArticleCategoryList '+ str(articles))
            # получить список данных
            
            self.render("rest/ctegory_list.html", dataList=articles,  itemName="category_article_id", selected=int(curentParameter))


        if commandName == 'getArticleTemplateList':

            if int(curentParameter) == 0:
                curentParameter = config.options.main_info_template

            articles = [Article(0, 'Выберите значение ')]
            artControl = ControlArticle()
            articles += yield executor.submit( artControl.getListArticles, config.options.tpl_categofy_id)
            logging.info('RestMinHandler:: commandName:: getArticleTemplateList '+ str(articles))
            # получить список данных

            self.render("rest/ctegory_list.html", dataList=articles, itemName="template_id", selected=int(curentParameter))





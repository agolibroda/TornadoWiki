#!/usr/bin/env python
#
# Copyright 2015 Alec Golibroda

#  чем по - идее, имею дело? 
#  дмин - это просмотр списка 
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


# A thread pool to be used for password hashing with bcrypt.
executor = concurrent.futures.ThreadPoolExecutor(2)


class AdminBaseHandler(tornado.web.RequestHandler):
#     @property
#     def db(self):
#         return self.application.db

    def get_current_user(self):
        try:
            user_id = int(self.get_secure_cookie("wiki_user"))
        except:
            user_id = 0
        logging.info('BaseHandler:: get_current_user:: user_id '+ str(user_id))
        if not user_id: return None
        user = User()
        user = user.get(user_id)
        logging.info('BaseHandler:: get_current_user:: user '+ str(user))

        return user

    def any_author_exists(self):
        return bool(self.get_current_user())



class AdminHomeHandler(AdminBaseHandler):
    """
    росмотреть списк материалов
    при просмотре каждого материала открываем по ИД мтатьи
    просматриваем только актуальные версии
    """
    
    @tornado.web.authenticated
    @gen.coroutine
    def get(self):
        logging.info( 'AdminHomeHandler:: get ')
        artControl = ControlArticle()
        articles = yield executor.submit( artControl.getListArticles )

        self.render(config.options.adminTplPath+"articles.html", articles=articles)



class AdminFeedHandler(AdminBaseHandler):
    """
    просмотр списка материалов в другом формате
    - стоит сделать вызов процедуры из хелпера.
    
    """
    @tornado.web.authenticated
    @gen.coroutine
    def get(self):

        artControl = ControlArticle()
        articles = yield executor.submit( artControl.getListArticles )
        self.set_header("Content-Type", "application/atom+xml")
        self.render(config.options.adminTplPath+"feed.xml", articles=articles)



class AdminArticleHandler(AdminBaseHandler):
    """
    просмотр одной статьи - открываем по ИД (не по заголовку (как в пользовательском интерфейсе вики) )
    
    """
    @tornado.web.authenticated
    @gen.coroutine
    def get(self, articleId):
        
        artModel = Article()
        
        artControl = ControlArticle()
        (article, fileList) = yield executor.submit( artControl.getArticleById, articleId )
        logging.info( 'ArticleHandler:: article = ' + str(article))
        logging.info( 'AdminHomeHandler:: fileList = ' + str(fileList))

        if not article: raise tornado.web.HTTPError(404)
        wrkTpl = config.options.adminTplPath+"article.html"
        logging.info( 'AdminHomeHandler:: wrkTpl = ' + str(wrkTpl))
        
        self.render( wrkTpl, article=article, fileList=fileList)




class AdminRevisionsHandler(AdminBaseHandler):
    @gen.coroutine
    def get(self):
        articleId = self.get_argument("id", None)
        artModel = Article()
        articles = yield executor.submit( artModel.revisionsList, articleId)
        if not articles:
            self.redirect(config.options.adminPath + "/compose")
            return
        self.render(config.options.adminTplPath+"revisions.html", articles=articles)
   


class AdminRevisionViewHandler(AdminBaseHandler):
    """
    Показать список ревизий для 
    """
    @gen.coroutine
    def get(self):

        articleId = self.get_argument("aid", None)
        revId = self.get_argument("rid", None)
        
        revModel = Revision()
        revision = yield executor.submit( revModel.get2Edit, articleId, revId )

        logging.info( 'RevisionViewHandler:: revision = ' + str(revision))
        self.render(config.options.adminTplPath+"revision.html", revision=revision)



class AdminComposeHandler(AdminBaseHandler):
    """
    редактирование статьи с правами админа 
    - расширенное количество типов (м.б.)
    - может возможностоь менять "category_article_id" фактически - 
        "тип статьи" 
        - шаблон 
        - статья категория
        - инфрмационная статья 
    """
    @tornado.web.authenticated
    @gen.coroutine
    def get(self):
 
        articleId = self.get_argument("aid", None)
        revId = self.get_argument("rid", None)
        article = None
        fileList = []

        if articleId and revId:
            artControl = ControlArticle()
            (article, fileList) = yield executor.submit( artControl.getArticleByIdRevId, articleId, revId ) 
#             logging.info( 'ComposeHandler:: get article = ' + str(article))
        self.render(config.options.adminTplPath+"compose.html", article=article,  fileList=fileList, isCkEditMake=False)

    @tornado.web.authenticated
    @gen.coroutine
    def post(self):

        artModel = Article()

        curentUser = yield executor.submit(self.get_current_user ) #self.get_current_user ()
#         logging.info( 'ComposeHandler:: post rezult = ' + str(rezult))
#         curentUser = rezult.result()
        
        if not curentUser.user_id: return False


        artModel.article_id = self.get_argument("id", 0)
        artModel.article_title = self.get_argument("article_title")
        artModel.article_annotation = self.get_argument("article_annotation")
        artModel.article_html = self.get_argument("article_html")
        
        rez = yield executor.submit( artModel.save, curentUser.user_id )
        
        if rez:
#             self.redirect("/article/" + tornado.escape.url_escape( artModel.article_link))
#  artModel.getById, articleId 
            self.redirect(config.options.adminTplPath+"/article/" + tornado.escape.url_escape( artModel.article_link))
        else:
            logging.info( 'ComposeHandler:: rez = ' + str(rez))
#             как - то надо передать данные и ошибку - что - то пошло же не так... 
#             да, и можно и ошибку то получить... 
#             тоько КАК  - если эксепшин тут не работает... :-( )
#             self.redirect("/compose" ) 


#############################################

class ArticleModule(tornado.web.UIModule):
    def render(self, article, fileList):
#         logging.info( 'ArticleModule:: fileList = ' + str(fileList))
        return self.render_string(config.options.adminTplPath+"modules/article.html", article=article, fileList=fileList)


class FilesListModule(tornado.web.UIModule):
    def render(self, fileList):
        logging.info( 'FilesList:: fileList = ' + str(fileList))
        return self.render_string(config.options.adminTplPath+"modules/files_list.html", fileList=fileList)

class RevisionModule(tornado.web.UIModule):
    def render(self, revision):
        return self.render_string(config.options.adminTplPath+"modules/revision.html", revision=revision)



class SimpleArticleModule(tornado.web.UIModule):
    def render(self, article):
        return self.render_string(config.options.adminTplPath+"modules/simple_article.html", article=article)




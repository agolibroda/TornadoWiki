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

from core.models.template   import Template


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
        logging.info('AdminBaseHandler:: get_current_user:: user_id '+ str(user_id))
        if not user_id: return None
        user = User()
        user = user.get(user_id)
#         logging.info('AdminBaseHandler:: get_current_user:: user '+ str(user))

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
        try:
            logging.info( 'AdminHomeHandler:: get ')
            artControl = ControlArticle()
            articles = yield executor.submit( artControl.getListArticles )
    
            self.render(config.options.adminTplPath+"articles.html", articles=articles, tplCategory=config.options.tpl_categofy_id )
        except Exception as e:
            logging.info( 'Save:: Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.render('error.html', error=error)


class AdminHomeArticlesCategory(AdminBaseHandler):
    """
    получить список всех статей одной категори
    
    """
    
    @tornado.web.authenticated
    @gen.coroutine
    def get(self, categoryId):
        try:
            logging.info( 'AdminHomeArticlesCategory:: get ')
            artControl = ControlArticle()
            articles = yield executor.submit( artControl.getListArticlesCategory, categoryId)
    
            self.render(config.options.adminTplPath+"articles.html", articles=articles)
        except Exception as e:
            logging.info( 'Save:: Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.render('error.html', error=error)



class AdminFeedHandler(AdminBaseHandler):
    """
    просмотр списка материалов в другом формате
    - стоит сделать вызов процедуры из хелпера.
    
    """
    @tornado.web.authenticated
    @gen.coroutine
    def get(self):
        try:
            artControl = ControlArticle()
            articles = yield executor.submit( artControl.getListArticles )
            self.set_header("Content-Type", "application/atom+xml")
            self.render(config.options.adminTplPath+"feed.xml", articles=articles)
        except Exception as e:
            logging.info( 'Save:: Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.render('error.html', error=error)



class AdminArticleHandler(AdminBaseHandler):
    """
    просмотр одной статьи - открываем по ИД (не по заголовку (как в пользовательском интерфейсе вики) )
    
    """
    @tornado.web.authenticated
    @gen.coroutine
    def get(self, articleId):
        try:
            artModel = Article()
            
            artControl = ControlArticle()
            (article, fileList) = yield executor.submit( artControl.getArticleById, articleId )
    #         logging.info( 'AdminArticleHandler:: fileList = ' + str(fileList))
    
            if not article: raise tornado.web.HTTPError(404)
            wrkTpl = config.options.adminTplPath+"article.html"
    
            logging.info( 'AdminArticleHandler:: article = ' + str(article))
            logging.info( 'AdminArticleHandler:: wrkTpl = ' + str(wrkTpl))
            
            self.render( wrkTpl, article=article, fileList=fileList)
        except Exception as e:
            logging.info( 'Save:: Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.render('error.html', error=error)




class AdminRevisionsHandler(AdminBaseHandler):
    @gen.coroutine
    def get(self):
        try:
            articleId = self.get_argument("id", None)
            artModel = Article()
            articles = yield executor.submit( artModel.revisionsList, articleId)
            if not articles:
                self.redirect(config.options.adminPath + "/compose")
                return
            self.render(config.options.adminTplPath+"revisions.html", articles=articles)
        except Exception as e:
            logging.info( 'Save:: Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.render('error.html', error=error)
   


class AdminRevisionViewHandler(AdminBaseHandler):
    """
    Показать список ревизий для 
    """
    @gen.coroutine
    def get(self):
        try:
            articleId = self.get_argument("aid", None)
            revId = self.get_argument("rid", None)
            
            revModel = Revision()
            revision = yield executor.submit( revModel.get2Edit, articleId, revId )
    
            logging.info( 'RevisionViewHandler:: revision = ' + str(revision))
            self.render(config.options.adminTplPath+"revision.html", revision=revision)
        except Exception as e:
            logging.info( 'Save:: Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.render('error.html', error=error)



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
        try:
            articleId = self.get_argument("aid", None)
            revId = self.get_argument("rid", None)
            logging.info( 'AdminComposeHandler:: self.get_argument("ned", 0) = ' + str(self.get_argument("ned", 0)))
            isNotEdit = self.get_argument("ned", 0)
            logging.info( 'AdminComposeHandler:: isNotEdit = ' + str(isNotEdit))
            article = Article()
            fileList = []
    
            if articleId and revId:
                artControl = ControlArticle()
                (article, fileList) = yield executor.submit( artControl.getArticleByIdRevId, articleId, revId ) 
                logging.info( 'AdminComposeHandler:: get article = ' + str(article))
            article.tpl_categofy_id = config.options.info_page_categofy_id 
            self.render(config.options.adminTplPath+"compose.html", article=article,  fileList=fileList, isCkEditMake=isNotEdit)
        except Exception as e:
            logging.info( 'Save:: Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.render('error.html', error=error)

    @tornado.web.authenticated
    @gen.coroutine
    def post(self):
        try:
            artModel = Article()
    
            curentUser = yield executor.submit(self.get_current_user ) #self.get_current_user ()
    #         logging.info( 'AdminComposeHandler:: post rezult = ' + str(rezult))
    #         curentUser = rezult.result()
            
            if not curentUser.user_id: return False
    
            artModel.article_id = self.get_argument("id", 0)
            artModel.article_title = self.get_argument("article_title")
            artModel.article_annotation = self.get_argument("article_annotation")
            artModel.article_html = self.get_argument("article_html")
            artModel.category_article_id = self.get_argument("category_article_id", 0)
            artModel.template = int(self.get_argument("template_id", 0))
            logging.info( 'AdminComposeHandler:: Before Save! artModel = ' + str(artModel))
    
            article_link =  artModel.article_title.lower().replace(' ','_')
            
            templateDir = self.get_template_path()
            
            rez = yield executor.submit( artModel.save, curentUser.user_id, templateDir )
            logging.info( 'AdminComposeHandler:: rez = ' + str(rez))
            
            redirectLink = "/"+config.options.adminTplPath + 'article/' + str(rez.article_id) # article_link
            logging.info( 'AdminComposeHandler:: redirectLink = ' + str(redirectLink))
            self.redirect( redirectLink )
    
        except Exception as e:
            logging.info( 'Save:: Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.render('error.html', error=error)


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




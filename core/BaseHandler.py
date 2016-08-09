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

import config

import core.models

from core.models.user import User
from core.models.article import Article
from core.models.article import Revision
from core.models.file import File

from core.control.article import ControlArticle 



# A thread pool to be used for password hashing with bcrypt.
executor = concurrent.futures.ThreadPoolExecutor(2)


class BaseHandler(tornado.web.RequestHandler):
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



class HomeHandler(BaseHandler):
    """
    вот именно тут наверое, надо загружать нужную нам страницу по ее ИД
    - с получением ее ИД щаблона, и грузить и шаблон тоже. 
    - причем, шаблон со всяческими там проверками - есть или нет, и, если есть, тогда 
    вынуть шаблон из какой - то особой папки...
    - если шаблона там етути, тогда его туда положить... 
    ну, как  - то так... 
    а пока... 
    займусь админкой.. 
    может и редактор статей сделать частью админовского слоя?
    
    """

    @gen.coroutine
    def get(self):
        
        
        articleId = config.options.main_page_id
        
        artControl = ControlArticle()
        (article, fileList) = yield executor.submit( artControl.getArticleById, articleId)

        logging.info( 'ArticleHandler:: fileList = ' + str(fileList))
        
        self.render("admin/article.html", article=article, fileList=fileList)



class AlterHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        artModel = Article()
        articles = yield executor.submit( artModel.list )
        if not articles:
            self.redirect("/compose")
            return
        self.render("home.html", articles=articles)



class RevisionsHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        articleId = self.get_argument("id", None)
        artModel = Article()
        articles = yield executor.submit( artModel.revisionsList, articleId)
        if not articles:
            self.redirect("/compose")
            return
        self.render("revisions.html", articles=articles)
   
   

class RevisionViewHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        articleId = self.get_argument("aid", None)
        revId = self.get_argument("rid", None)
        revModel = Revision()
        revision = yield executor.submit( revModel.get2Edit, articleId, revId )
#         if not article:
#             self.redirect("/compose")
#             return
        fileControl = File()

        logging.info( 'RevisionViewHandler:: revision = ' + str(revision))
        self.render("revision.html", revision=revision)



class ArticleHandler(BaseHandler):
    """
    загрузка страницы по ее названию (линке) 
    может именно тут и менять пробелы на подчеркивания? 
    потом будет логичнее прописывать линки в тексте (как вижу, так и пою)
    это на "совсем потом" - тогда, когда надо будет делать новые страницы через 
    добавление линков на не существующие страницы
    
    """
    @gen.coroutine
    def get(self, articleName):


        artControl = ControlArticle()
        (article, fileList) = yield executor.submit( artControl.getArticleByName, articleName )
   
   # а вот тут я должен получить и распарсить шаблон - как - текст в статьях (особой категории!!!!)
        if not article: raise tornado.web.HTTPError(404)

        logging.info( 'ArticleHandler:: fileList = ' + str(fileList))
        
        self.render("article.html", article=article, fileList=fileList)





class ComposeHandler(BaseHandler):
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
        self.render("compose.html", article=article,  fileList=fileList)

    @tornado.web.authenticated
    @gen.coroutine
    def post(self):

        artModel = Article()

        curentUser = yield executor.submit(self.get_current_user ) #self.get_current_user ()
#         logging.info( 'ComposeHandler:: post rezult = ' + str(rezult))
#         curentUser = rezult.result()
        
        if not curentUser.user_id: return None


        artModel.article_id = self.get_argument("id", 0)
        artModel.article_title = self.get_argument("article_title")
        artModel.article_annotation = self.get_argument("article_annotation")
        artModel.article_html = self.get_argument("article_html")
        
#         try:
#             rez = yield executor.submit( artModel.save, curentUser.user_id )
#         except Exception as e:   
#             logging.info( 'ComposeHandler:: Exception as et = ' + str(e))
#             fileList = []
#             self.render("compose.html", article=artModel,  fileList=fileList) 
         
        rez = yield executor.submit( artModel.save, curentUser.user_id )
        
        if rez:
            self.redirect("/article/" + tornado.escape.url_escape( artModel.article_link))
        else:
            logging.info( 'ComposeHandler:: rez = ' + str(rez))
#             как - то надо передать данные и ошибку - что - то пошло же не так... 
#             да, и можно и ошибку то получить... 
#             тоько КАК  - если эксепшин тут не работает... :-( )
#             self.redirect("/compose" ) 


class AuthCreateHandler(BaseHandler):
    """
    содать нового автора 
    - страница регистрации пользователя
    """
    def get(self):
        self.render("create_author.html")

    @gen.coroutine
    def post(self):
        if self.any_author_exists():
            raise tornado.web.HTTPError(400, "author already created")
 
        userLoc =  User()
        userLoc.user_login = self.get_argument("name")
        userLoc.user_email = self.get_argument("email")
        userLoc.user_pass = self.get_argument("password")
        rez = yield executor.submit( userLoc.save )
        logging.info( 'AuthCreateHandler  post rez = ' + str(rez))
        
        self.set_secure_cookie("wiki_user", str(userLoc.user_id))
        self.redirect(self.get_argument("next", "/"))


class AuthLoginHandler(BaseHandler):
    def get(self):
        # If there are no authors, redirect to the account creation page.
#         if not self.any_author_exists():
#             self.redirect("/auth/create")
#         else:
        self.render("login.html", error=None)

    @gen.coroutine
    def post(self):
        userloginLoad =  User()

        rezult = yield executor.submit( userloginLoad.login, self.get_argument("login"), self.get_argument("password") )
        if rezult:
            logging.info( 'AuthLoginHandler  userloginLoad = ' + str(userloginLoad))
            
            self.set_secure_cookie("wiki_user", str(userloginLoad.user_id))
            self.redirect(self.get_argument("next", "/"))
        else:
            self.render("login.html", error="incorrect password")

#         self.db.get("SELECT * FROM authors WHERE email = %s",
#                              self.get_argument("email"))
#         if not author:
#             self.render("login.html", error="email not found")
#             return
#         hashed_password = yield executor.submit(
#             bcrypt.hashpw, tornado.escape.utf8(self.get_argument("password")),
#             tornado.escape.utf8(author.hashed_password))
#         if hashed_password == author.hashed_password:
#             self.set_secure_cookie("wiki_user", str(author.id))
#             self.redirect(self.get_argument("next", "/"))
#         else:
#             self.render("login.html", error="incorrect password")


class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("wiki_user")
        self.redirect(self.get_argument("next", "/"))




class UploadHandler(BaseHandler):
    """
    загрузка файлов... 
    открываем с ИД статьи в адресе 
    грузим файл/файлы, делаем записи в табличке файлы, 
    делаем записи в табличке "крос-линки" == привязываем картинки к статьям
    Если грузим файлы в документ ИД===0 
    значит, сразу открываем новую статью - имя статьи == имени файла, 
    ив крос-таблице ставим флаг == "М" - главная статья
    То есть, у нас есть файлы - к каждому файлу МОЖЕТ быть привязана статья описания - 
    и каждый файл может быть привязан к юольшому количеству разных статей. 
    
    """
    @tornado.web.authenticated
    def get(self, article_id):
#         article_id = self.get_argument("id", 0)
        logging.info( 'UploadHandler:: get article_id =  ' + str(article_id) )
        self.article_id = article_id
        self.render("upload.html", error=None, article_id = article_id)
    
    
    @gen.coroutine
    @tornado.web.authenticated
    def post(self, article_id):

        curentUser = yield executor.submit(self.get_current_user ) #self.get_current_user ()
#         logging.info( 'ComposeHandler:: post rezult = ' + str(rezult))
#         curentUser = rezult.result()
        
        user_id = curentUser.user_id
        
        fileContrl = File()
        fileInfo = yield executor.submit(
                                        fileContrl.upload, 
                                        self.request.files, #['filearg'], 
                                        article_id, user_id 
                                        ) 
#         fileInfo = fileContrl.upload(self.request.files, article_id, user_id ) 
#         for oneRez in fileInfo:
#             logging.info( 'UploadHandler:: post oneRez = '  + str(oneRez))
# 
#         if fileInfo.file_id != 0:
#             error = fileInfo.error # None
#         else:
#             error =  fileInfo.error #'error upload file'
#  вот тут надо послать некий сигнал, что все хорошо, и можно обновить 
# данными из fileInfo нужную панель в приемнике, пичем, почему бы ЭТО не сделать сокетами?
        error = None
#         self.finish("file" + fileContrl.originalFname + " is uploaded")
        self.redirect("/upload/" + article_id, error)



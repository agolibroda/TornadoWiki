#!/usr/bin/env python
#
# Copyright 2015 Alec Golibroda


#  Впринцепе, Это "тулБокс" - ящик с инструментами просто пользователя 
# надо сюда добавить 
# список ПОльзователей
# список Групп
#
# ArticleControl.py 


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
from core.models.template import Template

from core.helpers.article import HelperArticle 

from core.BaseHandler import *
from core.WikiException import *



# A thread pool to be used for password hashing with bcrypt.
executor = concurrent.futures.ThreadPoolExecutor(2)


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
        try:
            articleId = config.options.main_page_id
            
            artHelper = HelperArticle()
            (article, fileList) = yield executor.submit( artHelper.getArticleById, articleId)
            logging.info( 'HomeHandler get article = ' + str(article))
    
    #         templateName = "admin/article.html"
            templateName = os.path.join(config.options.tmpTplPath, str(article.template) + config.options.tplExtension)
            logging.info( 'HomeHandler get templateName = ' + str(templateName))
            self.render(templateName, article=article, fileList=fileList)
        except Exception as e:
            logging.info( 'Save:: Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.render('error.html', error=error)



class ArticleListHandler(BaseHandler):
    """
    получить список статей категории "информационная статья"
    для показа списка статей
    
    """
    @gen.coroutine
    def get(self):
        try:
            artHelper = HelperArticle()
            articles = yield executor.submit( artHelper.getListArticles, config.options.info_page_categofy_id )
            if not articles:
                self.redirect("/compose")
                return
            self.render("articles.html", articles=articles)
        except Exception as e:
            logging.info( 'Save:: Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.render('error.html', error=error)

# что - то здеся не то - 
# что - то тут надо поправить 
# и сделать в одной упаковке 
# или показужу одной отдельной категории (для пользователя)Б
# или, для Админов - или пару категорий, или все категрии статей  - это для суперадмина.

# class AdminHomeArticlesCategory(BaseHandler):
#     """
#     получить список всех статей одной категори
#     
#     """
#     
#     @tornado.web.authenticated
#     @gen.coroutine
#     def get(self, categoryId):
#         try:
#             logging.info( 'AdminHomeArticlesCategory:: get ')
#             artHelper = HelperArticle()
#             articles = yield executor.submit( artHelper.getListArticlesCategory, categoryId)
#     
#             self.render(config.options.adminTplPath+"articles.html", articles=articles)
#         except Exception as e:
#             logging.info( 'Save:: Exception as et = ' + str(e))
#             error = Error ('500', 'что - то пошло не так :-( ')
#             self.render('error.html', error=error)




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

        try:
            artHelper = HelperArticle()
            (article, fileList) = yield executor.submit( artHelper.getArticleByName, articleName )
       
       # а вот тут я должен получить и распарсить шаблон - как - текст в статьях (особой категории!!!!)
            if article.article_id == 0 : 
                self.redirect("/compose/" + articleName ) 
    
            templateName = os.path.join(config.options.tmpTplPath, str(article.template) + config.options.tplExtension)
    
            logging.info( 'ArticleHandler get templateName = ' + str(templateName))
            logging.info( 'ArticleHandler:: article = ' + str(article))
    
            self.render(templateName, article=article, fileList=fileList)
        except Exception as e:
            logging.info( 'Save:: Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.render('error.html', error=error)


class MyArticletHandler(BaseHandler):
    pass


class ComposeHandler(BaseHandler):
    @tornado.web.authenticated
    @gen.coroutine
    def get(self, articleName = ''):
        try:
            articleId = self.get_argument("aid", None)
            revId = self.get_argument("rid", None)
            article = None
            fileList = []
            artHelper = HelperArticle()
            artHelper.setArticleCategiry (config.options.info_page_categofy_id) 
            logging.info( 'ComposeHandler:: 1 artHelper.getModel() = ' + str(artHelper.getModel()))
            
            if articleId and revId:
                (article, fileList) = yield executor.submit( artHelper.getArticleByIdRevId, articleId, revId ) 
                artHelper.setModel(article)
            elif articleName != '':
                artHelper.setArticleTitle (articleName)
    #         else:
    #             pass    
             
            logging.info( 'ComposeHandler:: 2 artHelper.getModel() = ' + str(artHelper.getModel()))
    #             logging.info( 'ComposeHandler:: get article = ' + str(article))
            self.render("compose.html", article=artHelper.getModel(),  fileList=fileList)
        except Exception as e:
            logging.info( 'Save:: Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.render('error.html', error=error)


    @tornado.web.authenticated
    @gen.coroutine
    def post(self, articleName = ''):
        try:
            logging.info( 'ComposeHandler:: post articleName = ' + str(articleName))
    
            artModel = Article()
    
            curentAuthor = yield executor.submit(self.get_current_user ) #self.get_current_user ()
    #         logging.info( 'ComposeHandler:: post rezult = ' + str(rezult))
    #         curentAuthor = rezult.result()
            
            if not curentAuthor.author_id: return None
    
    
            artModel.article_id = int(self.get_argument("id", 0))
            artModel.article_title = self.get_argument("article_title")
            artModel.article_annotation = self.get_argument("article_annotation") # article_annotation
            artModel.article_html = self.get_argument("article_html") # article_html
            artModel.category_article_id = int(self.get_argument("category_article_id", 0))
            
    #         logging.info( 'ComposeHandler:: Before Save! artModel = ' + str(artModel))
            
            article_link =  artModel.article_title.lower().replace(' ','_')
            templateDir = self.get_template_path()
    
            rez = yield executor.submit( artModel.save, curentAuthor.author_id, templateDir )
    
    #         logging.info( 'ComposeHandler:: AFTER Save! artModel = ' + str(artModel))
            
            if rez:
                self.redirect("/" + tornado.escape.url_escape(article_link))
            else:
                logging.info( 'ComposeHandler:: rez = ' + str(rez))
    #             как - то надо передать данные и ошибку - что - то пошло же не так... 
    #             да, и можно и ошибку то получить... 
    #             тоько КАК  - если эксепшин тут не работает... :-( )
    #             self.redirect("/compose" ) 
        except Exception as e:
            logging.info( 'Save:: Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.render('error.html', error=error)


#############################################
# тут похоже, надо передумать, и сделать из ЭТОГО текста основняк....abs(x) 



class AdminComposeHandler(BaseHandler):
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
                artHelper = HelperArticle()
                (article, fileList) = yield executor.submit( artHelper.getArticleByIdRevId, articleId, revId ) 
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
    
            curentAuthor = yield executor.submit(self.get_current_user ) #self.get_current_user ()
    #         logging.info( 'AdminComposeHandler:: post rezult = ' + str(rezult))
    #         curentAuthor = rezult.result()
            
            if not curentAuthor.author_id: return False
    
            artModel.article_id = self.get_argument("id", 0)
            artModel.article_title = self.get_argument("article_title")
            artModel.article_annotation = self.get_argument("article_annotation")
            artModel.article_html = self.get_argument("article_html")
            artModel.category_article_id = self.get_argument("category_article_id", 0)
            artModel.template = int(self.get_argument("template_id", 0))
            logging.info( 'AdminComposeHandler:: Before Save! artModel = ' + str(artModel))
    
            article_link =  artModel.article_title.lower().replace(' ','_')
            
            templateDir = self.get_template_path()
            
            rez = yield executor.submit( artModel.save, curentAuthor.author_id, templateDir )
            logging.info( 'AdminComposeHandler:: rez = ' + str(rez))
            
            redirectLink = "/"+config.options.adminTplPath + 'article/' + str(rez.article_id) # article_link
            logging.info( 'AdminComposeHandler:: redirectLink = ' + str(redirectLink))
            self.redirect( redirectLink )
    
        except Exception as e:
            logging.info( 'Save:: Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.render('error.html', error=error)


#############################################




class RevisionsHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        try:
            articleId = self.get_argument("id", None)
            artModel = Article()
            articles = yield executor.submit( artModel.revisionsList, articleId)
            if not articles:
                self.redirect("/compose")
                return
            self.render("revisions.html", articles=articles)
        except Exception as e:
            logging.info( 'Save:: Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.render('error.html', error=error)
   
   

class RevisionViewHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        try:
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
        except Exception as e:
            logging.info( 'Save:: Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.render('error.html', error=error)





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
        try:
            curentAuthor = yield executor.submit(self.get_current_user ) #self.get_current_user ()
    #         logging.info( 'ComposeHandler:: post rezult = ' + str(rezult))
    #         curentAuthor = rezult.result()
            
            author_id = curentAuthor.author_id
            
            fileContrl = File()
            fileInfo = yield executor.submit(
                                            fileContrl.upload, 
                                            self.request.files, #['filearg'], 
                                            article_id, author_id 
                                            ) 
    #         fileInfo = fileContrl.upload(self.request.files, article_id, author_id ) 
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
        except Exception as e:
            logging.info( 'Save:: Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.render('error.html', error=error)


class FeedHandler(BaseHandler):
    """
    просмотр списка материалов в другом формате
    - стоит сделать вызов процедуры из хелпера.
    
    """
    @tornado.web.authenticated
    @gen.coroutine
    def get(self):
        try:
            artHelper = HelperArticle()
            articles = yield executor.submit( artHelper.getListArticles )
            self.set_header("Content-Type", "application/atom+xml")
            self.render("feed.xml", articles=articles)
        except Exception as e:
            logging.info( 'Save:: Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.render('error.html', error=error)




 
class ArticleModule(tornado.web.UIModule):
    def render(self, article, fileList):
#         logging.info( 'ArticleModule:: fileList = ' + str(fileList))
        return self.render_string("modules/article.html", article=article, fileList=fileList)
 
 
class FilesListModule(tornado.web.UIModule):
    def render(self, fileList):
        logging.info( 'FilesList:: fileList = ' + str(fileList))
        return self.render_string("modules/files_list.html", fileList=fileList)
 
class RevisionModule(tornado.web.UIModule):
    def render(self, revision):
        return self.render_string("modules/revision.html", revision=revision)
 
 
 
class SimpleArticleModule(tornado.web.UIModule):
    def render(self, article):
        return self.render_string("modules/simple_article.html", article=article)

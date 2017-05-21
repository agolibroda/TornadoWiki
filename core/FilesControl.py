#!/usr/bin/env python
#
# Copyright 2017 Alec Golibroda


#
# Делаем здесь контроллер по работе с файлами
# надо загружать и много (для статьи) 
# и по одному - для профиля пользователя
#
# FilesControl.py 


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
import traceback


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
    @gen.coroutine
    def get(self, article_id):
#         article_id = self.get_argument("id", 0)
        logging.info( 'UploadHandler:: get article_id =  ' + str(article_id) )
        curentAuthor = yield executor.submit(self.get_current_user ) 
        logging.info( 'MyProfileHandler GET :: curentAuthor = ' + str(curentAuthor))

        if not curentAuthor.author_id: raise tornado.web.HTTPError(404, "author not found")
        
        tplControl = TemplateParams()
#         tplControl.make(curentAuthor)
#         tplControl.page_name= curentAuthor.author_name + ' '+ curentAuthor.author_surname
#         tplControl.link='profile'
        tplControl.error=None
        tplControl.autor=curentAuthor
        tplControl.article_id=article_id

        
        self.article_id = article_id
        self.render("upload.html", parameters=tplControl )
    
    
    @gen.coroutine
    @tornado.web.authenticated
    def post(self, article_id):
        try:
            curentAuthor = yield executor.submit(self.get_current_user ) #self.get_current_user ()
    #         logging.info( 'ComposeHandler:: post rezult = ' + str(rezult))
    #         curentAuthor = rezult.result()
            
            
            fileContrl = File()
            fileInfo = yield executor.submit(
                                            fileContrl.upload, 
                                            self.request.files, #['filearg'], 
                                            article_id, 
                                            curentAuthor.author_id 
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
            self.render('error.html', error=error, link='/compose', page_name='Редактирование')



class FilesListModule(tornado.web.UIModule):
    def render(self, fileList):
        logging.info( 'FilesList:: fileList = ' + str(fileList))
        return self.render_string("modules/files_list.html", fileList=fileList, link='/compose', page_name='Редактирование')

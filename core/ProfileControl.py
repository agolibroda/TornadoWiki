#!/usr/bin/env python
#
# Copyright 2015 Alec Golibroda

# 
# 
# ProfileControl.py
# 
#  Набор контроллеров для работы с профилями пользоватеоей
 

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

from core.models.author         import Author

from core.BaseHandler           import *


# A thread pool to be used for password hashing with bcrypt.
executor = concurrent.futures.ThreadPoolExecutor(2)


class AuthCreateHandler(BaseHandler):
    """
    содать нового автора 
    - страница регистрации пользователя
    """
    def get(self):
        self.render("create_author.html",  page_name= 'Регистрация нового Автора')

    @gen.coroutine
    def post(self):
        try:
            if self.any_author_exists():
                raise tornado.web.HTTPError(400, "author already created")
     
            authorLoc =  Author()
            authorLoc.author_login = self.get_argument("name")
            authorLoc.author_email = self.get_argument("email")
            authorLoc.author_pass = self.get_argument("password")
            rez = yield executor.submit( authorLoc.save )
            logging.info( 'AuthCreateHandler  post rez = ' + str(rez))
            
            self.set_secure_cookie("wiki_author", str(authorLoc.author_id))
            self.redirect(self.get_argument("next", "/"))
        except Exception as e:
            logging.info( 'Save:: Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.render('error.html', error=error)


class AuthLoginHandler(BaseHandler):
    def get(self):
        self.render("login.html", error=None, page_name= 'Страница входа')

    @gen.coroutine
    def post(self):
        try:
            authorloginLoad =  Author()
    
            rezult = yield executor.submit( authorloginLoad.login, self.get_argument("login"), self.get_argument("password") )
            if rezult:
                logging.info( 'AuthLoginHandler  authorloginLoad = ' + str(authorloginLoad))
                
                self.set_secure_cookie("wiki_author", str(authorloginLoad.author_id))
                self.redirect(self.get_argument("next", "/perconal_desk_top"))
            else:
                self.render("login.html", error="incorrect password")
        except Exception as e:
            logging.info( 'Save:: Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.render('error.html', error=error)


class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("wiki_author")
        self.redirect(self.get_argument("next", "/"))





class MyProfileHandler(BaseHandler):
    """
    показать и отредектировать собственный профиль :-) 
    - поменять пароль.... 
    
    """
    
    @tornado.web.authenticated
    @gen.coroutine
    def get(self):
        """
        и шаблон должен быть что - то типа "АдминДома" -) 
        и набирать его... 
        или, набирать тот шаблон через вызовы реста? 
        ну да, тут  - просто шаблон (и проверку рав - а можно ли какретному пользователю Админить, и тогда  ))
        или 403  - нету правов, или шаблон "автозаполнялку..." 

        """
        try:

            curentAuthor = yield executor.submit(self.get_current_user ) 
            logging.info( 'MyProfileHandler GET :: curentAuthor = ' + str(curentAuthor))

            if not curentAuthor.author_id: raise tornado.web.HTTPError(404, "data not found")
            
            
            self.render("my_profile.html", autor=curentAuthor, link='profile', page_name=curentAuthor.author_name + ' '+ curentAuthor.author_surname )
        except Exception as e:
            logging.info( 'Save:: Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.render('error.html', error=error)





class AuthorProfile(BaseHandler):
    """
    показать профиль любого пользователя
    
    """
    @tornado.web.authenticated
    @gen.coroutine
    def get(self):
        """
        и шаблон должен быть что - то типа "просмотр данных пользователя" -) 

        """
        try:

            curentAuthor = yield executor.submit(self.get_current_user ) #self.get_current_user ()
    #         logging.info( 'ComposeHandler:: post rezult = ' + str(rezult))
    #         curentAuthor = rezult.result()
            
            if not curentAuthor.author_id: return None
            
            logging.info( 'AdminHomeHandler:: get ')
            artControl = ControlArticle()
            articles = yield executor.submit( artControl.getListArticles )
    
    
            self.render(config.options.adminTplPath+"my_profile.html", articles=articles )
        except Exception as e:
            logging.info( 'Save:: Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.render('error.html', error=error)





# 
# class ProfileHandler(BaseHandler):
#     pass



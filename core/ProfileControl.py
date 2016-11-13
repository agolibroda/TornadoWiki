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

from core.models.author       import Author

from core.BaseHandler import *


# A thread pool to be used for password hashing with bcrypt.
executor = concurrent.futures.ThreadPoolExecutor(2)




class AuthCreateHandler(BaseHandler):
    """
    содать нового автора 
    - страница регистрации пользователя
    """
    def get(self):
        self.render("create_author.html")

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
        # If there are no authors, redirect to the account creation page.
#         if not self.any_author_exists():
#             self.redirect("/auth/create")
#         else:
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
    
#     def initialize(self, flag):
#         logging.info( 'AdminHomeHandler:: __init__:: flag = ' + str(flag))
#         self.flag = flag

#     def __init__(self, flag):
#         """
#         """
#         logging.info( 'AdminHomeHandler:: __init__:: flag = ' + str(flag))
         
         
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
            logging.info( 'AdminHomeHandler:: get ')
            artControl = ControlArticle()
            articles = yield executor.submit( artControl.getListArticles )
    
    
            self.render(config.options.adminTplPath+"admin_home.html", articles=articles, tplCategory=config.options.tpl_categofy_id )
        except Exception as e:
            logging.info( 'Save:: Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.render('error.html', error=error)





class AuthorProfile(BaseHandler):
    """
    показать профиль любого пользователя
    
    """
    pass

# 
# class ProfileHandler(BaseHandler):
#     pass



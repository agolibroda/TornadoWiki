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

from core.models.user       import User

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
     
            userLoc =  User()
            userLoc.user_login = self.get_argument("name")
            userLoc.user_email = self.get_argument("email")
            userLoc.user_pass = self.get_argument("password")
            rez = yield executor.submit( userLoc.save )
            logging.info( 'AuthCreateHandler  post rez = ' + str(rez))
            
            self.set_secure_cookie("wiki_user", str(userLoc.user_id))
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
            userloginLoad =  User()
    
            rezult = yield executor.submit( userloginLoad.login, self.get_argument("login"), self.get_argument("password") )
            if rezult:
                logging.info( 'AuthLoginHandler  userloginLoad = ' + str(userloginLoad))
                
                self.set_secure_cookie("wiki_user", str(userloginLoad.user_id))
                self.redirect(self.get_argument("next", "/"))
            else:
                self.render("login.html", error="incorrect password")
        except Exception as e:
            logging.info( 'Save:: Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.render('error.html', error=error)

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





class UserProfile(BaseHandler):
    """
    показать профиль любого пользователя
    
    """
    pass

# 
# class ProfileHandler(BaseHandler):
#     pass


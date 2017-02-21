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

import copy

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
from core.WikiException         import *


# A thread pool to be used for password hashing with bcrypt.
executor = concurrent.futures.ThreadPoolExecutor(2)


class AuthCreateHandler(BaseHandler):
    """
    содать нового автора 
    - страница регистрации пользователя
    """
    def get(self):
        self.render("create_author.html", link='auth/create', page_name= 'Регистрация нового Автора', error='')

    @gen.coroutine
    def post(self):
        try:
#             if self.any_author_exists():
#                 raise tornado.web.HTTPError(400, "author already created")
     
            passwd = self.get_argument("pass")
            passwd2 = self.get_argument("pass_conf")
            if passwd != passwd2: 
#  надо добавить сообщение о том,что пароли не совпадают, и вывести эти сообщеия в правильном месте!!!!                
                error = Error ('500', 'Пароли не совпадают! ')
                raise WikiException(error ) 
                
            authorLoc =  Author()
            authorLoc.author_role = 'volunteer'
            
            authorLoc.author_login = self.get_argument("login")
            authorLoc.author_email = self.get_argument("email")
            authorLoc.author_pass = passwd
            
            authorLoc.author_name = self.get_argument("name")
            authorLoc.author_surname = self.get_argument("surname")
            authorLoc.author_phon = self.get_argument("phon")

            logging.info( 'AuthCreateHandler  post authorLoc = ' + str(authorLoc))
            
            rez = yield executor.submit( authorLoc.save )
            logging.info( 'AuthCreateHandler  post rez = ' + str(rez))
            
            self.set_secure_cookie("wiki_author", str(authorLoc.author_id))
            self.redirect(self.get_argument("next", "/"))
        except Exception as e:
            logging.info( 'Save:: Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.render("create_author.html", link='auth/create', page_name= 'Регистрация нового Автора', error=error)


class AuthLoginHandler(BaseHandler):
    def get(self):
        
        if self.get_current_user():
            self.redirect("/personal_desk_top")
        self.makeTplParametr()
        self.templateParams.page_name='Страница входа'
        self.templateParams.link='auth/login'
        self.templateParams.error=None
        logging.info( 'PersonalDeskTop:: self.templateParams ' + str(self.templateParams))
        
        self.render("login.html", parameters=self.templateParams)

    @gen.coroutine
    def post(self):
        try:
            authorloginLoad =  Author()
    
            rezult = yield executor.submit( authorloginLoad.login, self.get_argument("login"), self.get_argument("password") )
            if rezult:
                logging.info( 'AuthLoginHandler  authorloginLoad = ' + str(authorloginLoad))
                
                self.set_secure_cookie("wiki_author", str(authorloginLoad.author_id))
                self.redirect(self.get_argument("next", "/personal_desk_top"))
            else:
                self.render("login.html", error="incorrect login/password", link='auth/login', page_name= 'Страница входа')
        except Exception as e:
            logging.info( 'Save:: Exception as et = ' + str(e))
#             error = Error ('500', 'что - то пошло не так :-( ')
            self.render('login.html', error="incorrect password", link='auth/login', page_name= 'Страница входа')


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
            
            
            self.render("my_profile.html", autor=curentAuthor, link='profile', page_name=curentAuthor.author_name + ' '+ curentAuthor.author_surname, error='' )
        except Exception as e:
            logging.info( 'MyProfileHandler:: Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.render('error.html', error=error, link='profile', page_name=' Error Page ')

    @gen.coroutine
    def post(self):
        try:
#             if self.any_author_exists():
#                 raise tornado.web.HTTPError(400, "author already created")
 
            logging.info( 'MyProfileHandler  post pass !!!! = ' + str(self.get_argument("pass")))
            logging.info( 'MyProfileHandler  post pass_conf !!!! = ' + str(self.get_argument("pass_conf")))
            logging.info( 'MyProfileHandler  post login !!!! = ' + str(self.get_argument("login")))
            logging.info( 'MyProfileHandler  post email !!!! = ' + str(self.get_argument("email")))
            logging.info( 'MyProfileHandler  post name !!!! = ' + str(self.get_argument("name")))
            logging.info( 'MyProfileHandler  post surname !!!! = ' + str(self.get_argument("surname")))
            logging.info( 'MyProfileHandler  post phon !!!! = ' + str(self.get_argument("phon")))

            authorLoc = yield executor.submit(self.get_current_user ) 

            passwd = self.get_argument("pass")
            passwd2 = self.get_argument("pass_conf")
            if passwd != passwd2: 
#  надо добавить сообщение о том,что пароли не совпадают, и вывести эти сообщеия в правильном месте!!!!                
                error = Error ('500', 'Пароли не совпадают! ')
                raise WikiException( 'Пароли не совпадают! ' )  # Exception # 

      
#             authorLoc =  Author()
            
#             authorLoc.author_id = self.get_current_user
#             authorLoc.author_role = 'volunteer'
            
            authorLoc.author_login = self.get_argument("login")
            authorLoc.author_email = self.get_argument("email")

            authorLoc.author_pass = passwd
            
            authorLoc.author_name = self.get_argument("name")
            authorLoc.author_surname = self.get_argument("surname")
            authorLoc.author_phon = self.get_argument("phon")

            logging.info( 'MyProfileHandler  post authorLoc = ' + str(authorLoc))
            
            rez = yield executor.submit( authorLoc.save )
            logging.info( 'MyProfileHandler  post rez = ' + str(rez))
            
            self.set_secure_cookie("wiki_author", str(authorLoc.author_id))
            self.render("my_profile.html", autor=authorLoc, link='profile', page_name=authorLoc.author_name + ' '+ authorLoc.author_surname, error='' )
        except Exception as e:
            logging.info( 'MyProfileHandler Post:: Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            self.render("my_profile.html", autor=authorLoc, link='profile', page_name=authorLoc.author_name + ' '+ authorLoc.author_surname, error=str(e) )
 




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
            self.render('error.html', error=error, link='profile', page_name='Error Page')





# 
# class ProfileHandler(BaseHandler):
#     pass



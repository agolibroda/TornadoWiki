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

from core.models.article import Article



# A thread pool to be used for password hashing with bcrypt.
executor = concurrent.futures.ThreadPoolExecutor(2)


class AuthCreateHandler(BaseHandler):
    """
    содать нового автора 
    - страница регистрации пользователя
    """
    def get(self):

        tplControl = TemplateParams()
#         tplControl.make(self.autor)
        tplControl.page_name='Регистрация нового Автора'
        tplControl.link='auth/create'
        tplControl.error=None
        
        self.render("create_author.html", parameters=tplControl)

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

            tplControl = TemplateParams()
    #         tplControl.make(self.autor)
            tplControl.page_name='Регистрация нового Автора'
            tplControl.link='auth/create'
            tplControl.error=error
            
            self.render("create_author.html", parameters=tplControl)


class AuthLoginHandler(BaseHandler):
    def get(self):
        
        if self.get_current_user():
            self.redirect("/personal_desk_top")

        tplControl = TemplateParams()
#         tplControl.make(self.autor)
        tplControl.page_name='Страница входа'
        tplControl.link='auth/login'
        tplControl.error=None
        
        self.render("login.html", parameters=tplControl)

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
                raise WikiException( 'incorrect login/password' )
            
        except Exception as e:
            logging.info( 'AuthLoginHandler:: POST Exception as et = ' + str(e))

            tplControl.error="incorrect login/password"
            tplControl.link='auth/login'
            tplControl.page_name='Страница входа'
            self.render('login.html', parameters = tplControl )


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

            tplControl = TemplateParams()
            tplControl.make(self.autor)
            tplControl.page_name= curentAuthor.author_name + ' '+ curentAuthor.author_surname
            tplControl.link='profile'
            tplControl.error=None
            tplControl.autor=curentAuthor
            
            self.render("my_profile.html", parameters=tplControl)
            
        except Exception as e:
            logging.info( 'MyProfileHandler::GET Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            
            tplControl.error=error
            tplControl.link='/profile'
            tplControl.page_name=' Error Page '+ curentAuthor.author_name + ' '+ curentAuthor.author_surname
#             self.render('error.html', parameters = tplControl )
            self.render("my_profile.html", parameters=tplControl)

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
            
            tplControl = TemplateParams()
    #         tplControl.make(self.autor)
            tplControl.page_name = authorLoc.author_name + ' '+ authorLoc.author_surname
            tplControl.link='profile'
            tplControl.error=None
            tplControl.autor=authorLoc
            
            self.render("my_profile.html", parameters=tplControl)
        except Exception as e:
            logging.info( 'MyProfileHandler Post:: Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            
            tplControl.error=str(e)
            tplControl.link='/profile'
            tplControl.page_name = authorLoc.author_name + ' '+ authorLoc.author_surname
            tplControl.autor=authorLoc
            self.render('my_profile.html', parameters = tplControl )


class AuthorProfile(BaseHandler):
    """
    показать профиль любого пользователя
    Это надо показать и профиль пользователя (открытую часть)
    и список его статей (ПУБЛИЧНУЮ часть!!!!!)
    
    """
    @tornado.web.authenticated
    @gen.coroutine
    def get(self, presentAuthorId = 0):
        """
        и шаблон должен быть что - то типа "просмотр данных пользователя" -) 

        """
        try:
            # от его имени ведутся все расмотреня.... 
            spectatorAuthor = yield executor.submit(self.get_current_user ) #self.get_current_user ()
    #         logging.info( 'ComposeHandler:: post rezult = ' + str(rezult))
    #         curentAuthor = rezult.result()
            
            if not spectatorAuthor.author_id: return None
            
            logging.info( 'AdminHomeHandler:: get ')
            logging.info( 'AdminHomeHandler:: get presentAuthorId = ' + str (presentAuthorId))
#             presentAuthorId
# Надо загрузить описание пользователя ИД.... 
            
            artControl = Article()
            authorControl = Author()
            articles = yield executor.submit( artControl.listByAutorId, presentAuthorId, spectatorAuthor.author_id )
    
            tplControl = TemplateParams()
            tplControl.make(spectatorAuthor)
            tplControl.autor = yield executor.submit( authorControl.get, presentAuthorId )
            tplControl.articlesList= articles
#             да, надо найти пользователя по его ИД, и вот тут его передать в шаблон!
#             да и список пользовательских статей надо показать!!!!!!
#             падение черного ястреба
            
            tplControl.page_name='Page of Author '
            tplControl.link='profile'
            tplControl.error=None
            
            self.render("any_profile.html", parameters=tplControl)

        except Exception as e:
            logging.info( 'AuthorProfile:: GET Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            
            tplControl.error=error
            tplControl.link='profile'
            tplControl.page_name='Error Page'
            self.render('error.html', parameters = tplControl )





# 
# class ProfileHandler(BaseHandler):
#     pass



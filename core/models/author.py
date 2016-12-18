#!/usr/bin/env python
#
# Copyright 2015 Alec Goliboda
#
# authors.py

# from models.model import Model
# from model import Model

# from __future__ import print_function


import logging
import json

import config

# import pymysql
import bcrypt

import hashlib
import base64
from datetime import datetime

import tornado.options
import tornado.escape

from ..constants.data_base import *

from . import Model
# from .. import WikiException 
from core.WikiException import *


class Author(Model):

    def __init__ (self): 
#         logging.info('Author:: __init__')
        Model.__init__(self, 'authors')   

        self.author_id = 0
#         self.author_create = datetime.now()
        self.author_login = ''
        self.author_name  = '' 
        self.author_surname = ''
        self.author_role = ''
        self.author_phon = '' 
        self.author_email = ''
 
    def save(self):
        """
        сохранить значение - сохраняются все значимые (без подчеркивания) 
        свойства объекта
        пароль (новый,старый) перешифровывается 
        """
        if self.author_pass != '':
            bbsalt =  config.options.salt.encode()
            self.author_pass = bcrypt.hashpw( tornado.escape.utf8(self.author_pass),  bbsalt ).decode('utf-8') 
        if self.author_id == 0:
            self.author_create = datetime.now()
            self.author_id = self.insert('author_id')
            operationFlag = 'I'
        else:
            self.author_create =  datetime.fromtimestamp(int(self.author_create))
            logging.info(' save:: before Update = ' + str(self))
            self.update('author_id = ' + str(self.author_id))
            operationFlag = 'U'
            
        mainPrimaryObj = {'primaryName': 'author_id', 'primaryValue': self.author_id }
        revisions_sha_hash =  hashlib.sha256(
                    tornado.escape.utf8(self.author_login + self.author_name + self.author_surname + self.author_role +self.author_phon + self.author_email  )
                                            ).hexdigest() 
        logging.info(' save:: mainPrimaryObj = ' + str(mainPrimaryObj))
        self.saveRevision(self.author_id, operationFlag, mainPrimaryObj, revisions_sha_hash)
        return True
        
        

    def login(self, loginMailStr, pwdStr):
        """
        операция логина - 
        ли логин - 
        """
#         er = WikiException()
        if loginMailStr == '':
            raise WikiException(LOGIN_IS_ENPTY)
        if pwdStr != '':
            bbsalt =  config.options.salt.encode()
            test_pass = bcrypt.hashpw( tornado.escape.utf8(pwdStr),  bbsalt ).decode('utf-8') 
        else:
            raise WikiException(PASSWD_IS_ENPTY)

#         cur = self.db().cursor()
        selectStr = 'author_id,  author_login, author_name, author_surname, author_role, author_phon, author_email'
        fromStr = '' #'authors'
        anyParams = {
                    'whereStr': " (author_login =  '" + loginMailStr + "' OR author_email =  '" + loginMailStr + "' ) AND author_pass =  '"  + test_pass + "' " , 
                     }
        resList = self.select(selectStr, fromStr, anyParams)
        
        logging.info(' login:: resList = ' + str(resList))
        
        if len(resList) == 1:
            objValuesNameList = list(resList[0].__dict__.keys())
            for objValue in objValuesNameList:
                if objValue.find('_') != 0:
                    self.__setattr__(objValue,resList[0].__getattribute__(objValue) )
            return self
        else:
            raise WikiException(LOGIN_ERROR)


    def get(self, authorId):
        """
        загрузить ОДНО значение - по ИД пользователя
        """
        resList = self.select(
                    'author_id,  author_login, author_name,  author_surname, author_role, author_phon, author_email, floor(EXTRACT(EPOCH FROM author_create)) AS author_create ', # строка - чего хотим получить из селекта
                    '', #'authors',  # строка - список таблиц 
                    {
                     'whereStr': " author_id = " + str(authorId)
                     } #  все остальные секции селекта
                    )
#         logging.info('Author:: get:: resList = ')
#         logging.info(resList)
        if len(resList) == 1:
#             return resList[0]
            objValuesNameList = list(resList[0].__dict__.keys())
            for objValue in objValuesNameList:
                 if objValue.find('_') != 0:
                    self.__setattr__(objValue,resList[0].__getattribute__(objValue) )
            return self
        
        else:
            raise WikiException(LOAD_ONE_VALUE_ERROR)


    def list(self):
        cur = self.db().cursor()
        selectStr = 'author_id,  author_login, author_name,author_surname, author_role, author_phon, author_email, floor(EXTRACT(EPOCH FROM author_create)) AS author_create'
        fromStr = '' #'authors'
        anyParams = {
                    'orderStr': ' author_id', # строка порядок строк
                     }

        return self.select(selectStr, fromStr, anyParams)
 
       

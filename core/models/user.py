#!/usr/bin/env python
#
# Copyright 2015 Alec Goliboda
#
# users.py

# from models.model import Model
# from model import Model

# from __future__ import print_function


import logging
import json

import config

# import pymysql
import bcrypt

import tornado.options
import tornado.escape

from ..constants.data_base import *

from . import Model
from . import err


class User(Model):

    def __init__ (self): 
#         logging.info('User:: __init__')
        Model.__init__(self, 'users')   

        self.user_id = 0
        self.user_login = ''
        self.user_name  = '' 
        self.user_role = ''
        self.user_phon = '' 
        self.user_email = ''
        self.user_external = ''
 
    def save(self):
        """
        сохранить значение - сохраняются все значимые (без подчеркивания) 
        свойства объекта
        пароль (новый,старый) перешифровывается 
        """
        if self.user_pass != '':
            bbsalt =  config.options.salt.encode()
            self.user_pass = bcrypt.hashpw( tornado.escape.utf8(self.user_pass),  bbsalt ).decode('utf-8') 
        if self.user_id == 0:
            self.user_id = self.insert('user_id')
        else:
            self.update('user_id = ' + str(self.user_id))
        return True
        
        

    def login(self, loginMailStr, pwdStr):
        """
        операция логина - 
        ли логин - 
        """
        if loginMailStr == '':
            raise err.WikiException(LOGIN_IS_ENPTY)
        if pwdStr != '':
            bbsalt =  config.options.salt.encode()
            test_pass = bcrypt.hashpw( tornado.escape.utf8(pwdStr),  bbsalt ).decode('utf-8') 
        else:
            raise err.WikiException(PASSWD_IS_ENPTY)

#         cur = self.db().cursor()
        selectStr = 'user_id,  user_login, user_name, user_role, user_phon, user_email, user_external'
        fromStr = '' #'users'
        anyParams = {
                    'whereStr': " (user_login =  '" + loginMailStr + "' OR user_email =  '" + loginMailStr + "' ) AND user_pass =  '"  + test_pass + "' " , 
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
            raise err.WikiException(LOGIN_ERROR)


    def get(self, userId):
        """
        загрузить ОДНО значение - по ИД пользователя
        """
        resList = self.select(
                    'user_id,  user_login, user_name, user_role, user_phon, user_email user_external ', # строка - чего хотим получить из селекта
                    '', #'users',  # строка - список таблиц 
                    {
                     'whereStr': "  user_id = " + str(userId)
                     } #  все остальные секции селекта
                    )
#         logging.info('User:: get:: resList = ')
#         logging.info(resList)
        if len(resList) == 1:
#             return resList[0]
            objValuesNameList = list(resList[0].__dict__.keys())
            for objValue in objValuesNameList:
                 if objValue.find('_') != 0:
                    self.__setattr__(objValue,resList[0].__getattribute__(objValue) )
            return self
        
        else:
            raise err.WikiException(LOAD_ONE_VALUE_ERROR)


    def list(self):
        cur = self.db().cursor()
        selectStr = 'user_id,  user_login, user_name, user_role, user_phon, user_email, user_external'
        fromStr = '' #'users'
        anyParams = {
                    'orderStr': ' user_id', # строка порядок строк
                     }

        return self.select(selectStr, fromStr, anyParams)
 
       

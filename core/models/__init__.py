#!/usr/bin/env python
#
# Copyright 2015 Alec Goliboda
#
# users.py

# from models.model import Model
# from model import Model

from __future__ import print_function


import logging
import json

from tornado import gen

import tornado.options

import pymysql
from _ast import Try


#############
import config
from .. import err

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

# синглетон нужен для того, что бы все потредители ходил в базу через одн курсор, все здорово, 
# НО, если несколько потербителей пойдут в базу одновременно с разны нитей, получится кавардак :-( )
# в общем, надо или убирать "одиночку" + открывать МНОГО конектов к базе  - один конект - один курсор
# или, искать новый дравер, который сможет работать с несколькими курсорами, в одном конекте. 

# @singleton 
class Connector:
    def __init__ (self):    
        self._db = pymysql.connect(
                                    host =      config.options.mysql_host, #'127.0.0.1', 
#                                     port=       config.options.mysql_port, #3306, 
                                    user=       config.options.mysql_user, #'root', 
                                    passwd=     config.options.mysql_password, #'', 
                                    db=         config.options.mysql_db, #'blog'
                                    charset=    config.options.mysql_charset,
#                                   init_command=None,
#                                   init_command=' SET storage_engine=INNODB, SESSION TRANSACTION ISOLATION LEVEL SERIALIZABLE ',
#                                   init_command=' SET storage_engine=INNODB, SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED ',
#                                   init_command=' SET storage_engine=INNODB, SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ ',
                                    cursorclass=pymysql.cursors.DictCursor
                                    )
    



class Model: #Connector:

#     @property
    def __init__ (self, tabName ):    
        connector = Connector()
        self._db = connector._db
        self._tabName = tabName 
#         

#     def __del__(self):
#         self._db.close()
    
    
#     @property
    def db(self):
        return self._db

    def start_transaction(self):
        """
        START TRANSACTION;

        """
        self._db.begin()

    def commit(self):
        """
        commit;

        """
        self._db.commit()

    def rollback(self):
        """
        rollback;

        """
        self._db.rollback()

    
    def insert(self,  requestParamName = ''):
        """
        добавить в таблицу "tabName"  атрибуты класса, 
        вернуть максимальный ИД, если requestParamName не нудЁвый. 
        """
        try:
            lCurs = self._db.cursor()
            if requestParamName != '':
                del self.__dict__[requestParamName]
            paramsObj = self.splitAttributes()
            
            sqlStr = 'INSERT INTO ' + self._tabName +' ( ' + paramsObj.strListAttrNames + ' ) VALUES ( ' + paramsObj.strListAttrValues + ' )'
            logging.info(' insert:: sqlStr = ' + sqlStr)
            lCurs.execute(sqlStr)
            
            if requestParamName != '':
                
                self.commit()
#                 requestParamValue = None
#                 lCurs.execute('SELECT @@tx_isolation;')
#                 sourse = lCurs.fetchone() # .fetchall()
#                 logging.info(' insert:: SELECT @@tx_isolation; = ' + str(sourse))

                listSet = map(lambda x, y: str(x) + ' = "' + str(y) + '"', paramsObj.listAttrNames, paramsObj.listAttrValues)
                strWhere =  ' AND '.join(listSet)
                strQuery = "SELECT " + requestParamName +" AS " + requestParamName +" FROM "+ self._tabName +" WHERE " + strWhere + " ORDER BY "+ requestParamName +" DESC LIMIT 0,1 FOR UPDATE " 
                logging.info(' insert::MAXID!:: strQuery = ' + strQuery)
                lCurs.execute(strQuery)
                sourse = lCurs.fetchone() # .fetchall()
                self.__dict__[requestParamName] = sourse[requestParamName]
                self.commit()
                return  sourse[requestParamName]
#                 logging.info(' insert:: self = ' + str(self))
            self.commit()
        except pymysql.MySQLError as error:
            logging.error (' insert exception:: ' + str (error) )
            logging.error(' insert exception:: sqlStr = ' + sqlStr )
#             self.rollback() #execute('ROLLBACK')
#             lCurs.close()
            raise err.WikiException(error)
#         lCurs.execute('COMMIT')


    def update(self, whereSection):
        """
        изменить данные в таблицу "tabName"  атрибуты класса, 
        вернуть максимальный ИД, если requestParamName не нудЁвый. 
        """
        try:
            
            lCurs = self._db.cursor()
            paramsObj = self.splitAttributes()
            listSet = map(lambda x, y: str(x) + ' = "' + str(y) + '"', paramsObj.listAttrNames, paramsObj.listAttrValues)
            strSet =  ', '.join(listSet)
            sqlStr = 'UPDATE '+ self._tabName +' SET ' + strSet + ' WHERE ' + whereSection
            logging.info(' update:: sqlStr = ' + sqlStr)
            lCurs.execute(sqlStr)
            self.commit()
        except pymysql.MySQLError as error:
            logging.error(' update exception:: ' + str (error) )
            logging.error(' update exception:: sqlStr = ' + sqlStr )
#             self.rollback() #execute('ROLLBACK')
#             lCurs.close()
            raise err.WikiException(error)

    def select(self, 
               selectStr, # строка - чего хотим получить из селекта
               addTables,  # строка - список ДОПОЛНИТЕЛЬНЫХ таблиц (основную таблизу для объекта указываем при инициализации) 
               anyParams = {} #  все остальные секции селекта
               ):
        """
        получить данные (select)
        - ну, вынести его - и делать его из нескольких секций: 
        - селект (набор полей, котрые хотим получить из выборки)
        - фром  (набор дополнительных (кроме основной) таблиц для выборк)

               anyParams = {
                           'joinStr': '', # строка - список присоединенных таблиц
                           'whereStr': '', # строка набор условий для выбора строк
                           'groupStr': '', # строка группировка 
                           'orderStr': '', # строка порядок строк
                           'limitStr': '' # строка страница выборки
                            }
        - жоин
        - веа
        - ордер
        - групп
        - лимит вот как то так,  
        общий вид селекта, может выглядеть примерно так:
        SELECT 
            users.user_id,  
            users.user_login, 
            users.user_name, 
            users.user_role, 
            users.user_phon, 
            users.user_email, 
            users.user_external 
        FROM users 
        WHERE (user_login =  "login" OR user_email =  "login" ) 
        AND user_pass =  "$2b$12$.b9454ab5a22859b68bb4uvIvIvpREbnd9t2DJ7rqm1bwB/PrsH0." 
        
              
        """
        try:
#             logging.info(' select:: addTables = ' + str(addTables))
            cur = self._db.cursor()
            sqlStr = 'SELECT '+ selectStr
            if addTables != None:
                sqlStr += ' FROM ' + self._tabName 
            
#             if addTables == '':
#                 sqlStr += ' FROM ' + self._tabName 
                
                if addTables  != '':  sqlStr += ', ' + str(addTables)
                
            if str(anyParams.get('joinStr', ''))     != '':  sqlStr += ' ' + str(anyParams.get('joinStr'))
            if str(anyParams.get('whereStr', ''))    != '':  sqlStr += ' WHERE ' + str(anyParams.get('whereStr'))
            if str(anyParams.get('groupStr', ''))    != '':  sqlStr += ' GROUP BY ' + str(anyParams.get('groupStr'))
            if str(anyParams.get('orderStr', ''))    != '':  sqlStr += ' ORDER BY ' + str(anyParams.get('orderStr'))
            if str(anyParams.get('limitStr', ''))    != '':  sqlStr += ' LIMIT ' + str(anyParams.get('limitStr'))
            logging.info(' select:: sqlStr = ' + sqlStr)
            cur.execute(sqlStr)
            sourse = cur.fetchall()
            logging.info('select:: list:: sourse = ' + str (sourse) )
            cur.close()
            outListObj = self.dict2obj(sourse)    
            return outListObj

        except pymysql.MySQLError as error:
            logging.error(' update exception:: ' + str (error) )
            logging.error(' update exception:: sqlStr = ' + sqlStr )
            cur.close()
            raise err.WikiException(error)


    def splitAttributes(self):
        """
        разделить собственные параметры (без параметров с подчеркиваниями ) на 2 списка - 
        1 - список имен параметров
        2 - значений параметров 
        это нужно для того, что бы использовать все параметры в операции 
        добавления или изменения данных в базе данных.
        
        На выходе получим словарь из двух списков  
        """ 
        objDict = self.__dict__
        objValuesNameList = list(self.__dict__.keys())
        listAttrNames = []
        listAttrValues = []        
        for objValue in objValuesNameList:
            if objValue.find('_') != 0:
                listAttrNames.append(objValue)
                listAttrValues.append(self.__getattribute__(objValue))

        
        class Out: pass   
        out = Out()
        out.listAttrNames = listAttrNames
        out.listAttrValues = listAttrValues    
        out.strListAttrNames = ', '.join(listAttrNames)
        out.strListAttrValues = '"' + '", "'.join(map(str,listAttrValues)) + '"'   
#         out.strListAttrValues = '"' + '", "'.join(listAttrValues) + '"'   
        return out


    def dict2obj(self, dictSou):
        """
        преобразовать словарь (допустим, кортеж данных из селекта) в объект  
        """ 
        oList = []
        for row in dictSou:
            oneObj = self.__class__()
            for key in row.items(): #.__getattribute__(name):
                oneObj.__setattr__(key[0], key[1])
            oList.append(oneObj)
                
        return oList


    def __str__(self): 
        attribList = self.splitAttributes()
        className = str(self.__class__)
        itemsList = map(lambda x, y: ' "' + str(x) + '"' + ': "' + str(y) + '" ', attribList.listAttrNames, attribList.listAttrValues) 
        objValuesNameList = '\n'+ className + ': { \n\t' + ', \n\t'.join(itemsList) + '\n}'
        return objValuesNameList


# class Model(Connector):
# 
#     def __init__ (self, tabName):    
# #         logging.info('Model:: __init__:: make init ')
#         Connector.__init__(self, tabName)
   




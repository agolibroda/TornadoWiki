#!/usr/bin/env python
#
# Copyright 2015 Alec Goliboda
#
# 


# from models.model import Model
# from model import Model

from __future__ import print_function


import logging
import json

from tornado import gen

import tornado.options

# http://initd.org/psycopg/docs/index.html
import psycopg2

# from somewhere import namedtuple
import collections
# collections.namedtuple = namedtuple
# from psycopg2.extras import NamedTupleConnection
from psycopg2.extras import DictCursor
# NamedTupleCursor




from _ast import Try


#############
import config
# from .. import err
from .. import WikiException 

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

@singleton 
class Connector:
    def __init__ (self):    
        """
        # Connect to an existing database
        """
        self._connectInstans = psycopg2.connect(
                                                database= config.options.postgreBase, 
                                                host= config.options.postgreHost,
                                                port= config.options.postgrePort,
                                                user= config.options.postgreUser, 
                                                password= config.options.postgrePwd
                                                )
#         self._cursor = self._connectInstans.cursor(cursor_factory=NamedTupleCursor) DictCursor
        self._cursor = self._connectInstans.cursor(cursor_factory=DictCursor) 
    
    def getCursor (self):
        return self._cursor




class Model: #Connector:
    """
    # Набор методов для  работы с Ревизиями!
    # - добавит ревизию
    # - получить список ревизий
    # - получить оду ревизию...
    # - узнать является ли набор данных уникальным (не похожим на текущее значение данных - значит, у нас возможны циклы!!!!!)

    """

#     @property
    def __init__ (self, tabName ):    
        connector = Connector()
        self._cursor = connector.getCursor()
        self._tabName = tabName 

#     def __del__(self):
#         self._cursor.close()
    
    
#     @property
    def cursor(self):
        return self._cursor

    def begin(self, isolation= 'READ COMMITTED'):
        """
        START TRANSACTION;
        отдаем объект, который и будет делать все, до окончания трансакции 

        """
#         self._cursor.begin()
        self._cursor.execute("BEGIN")     
#         return self._cursor.xact(isolation)
#         self._cursor.xact(isolation)


    def commit(self):
        """
        commit;

        """
        self._cursor.execute("COMMIT")     
#         self._cursor.commit()   


# а вот так все описывается в документации!!!!!
# 
# 
# BEGIN;
# UPDATE accounts SET balance = balance + 100.00 WHERE acctnum = 12345;
# UPDATE accounts SET balance = balance - 100.00 WHERE acctnum = 7534;
# COMMIT;
#             self.rollback()
# 
#         self.begin()

    def rollback(self):
        """
        rollback;

        """
        self._cursor.execute("ROLLBACK")  
#         self._cursor.rollback()   


                
    def insert(self, autorId, requestParamName = ''):
        """
        добавить в таблицу "tabName"  атрибуты класса, 
        вернуть максимальный ИД, если requestParamName не пустой. 
        
        autorId - Это АВТОР РЕВИЗИИ - тот, кто делает конкретную запись!!!!!!
        requestParamName - название столбца, который является "автоинкрементным",  
        
        """
        try:
            lCurs = self.cursor()
            if requestParamName != '':
                del self.__dict__[requestParamName]
            paramsObj = self.splitAttributes()
            
            if requestParamName != '':
                sqlStr = "INSERT INTO " + self._tabName +" ( " + paramsObj.strListAttrNames + " ) VALUES ( " + paramsObj.strListAttrValues + " )  returning " + requestParamName
                logging.info(' insert:: sqlStr = ' + sqlStr)
                lCurs.execute(sqlStr)
                sourse = lCurs.fetchall()
                self.__dict__[requestParamName] = sourse[requestParamName]
                return  sourse[requestParamName]
            else:
                sqlStr = "INSERT INTO " + self._tabName +" ( " + paramsObj.strListAttrNames + " ) VALUES ( " + paramsObj.strListAttrValues + " )"
                logging.info(' insert:: sqlStr = ' + sqlStr)
                lCurs.execute(sqlStr)
                
            self.saverevision(autorId, 'I')
            
        except psycopg2.Error as error:
            
            logging.error (' insert exception:: ' + str (error) )
            logging.error(' insert exception:: sqlStr = ' + sqlStr )
            lCurs.rollback()
            raise err.WikiException(error)


    def update(self, autorId, whereSection):
        """
        изменить данные в таблицу "tabName"  атрибуты класса, 
        вернуть максимальный ИД, если requestParamName не нудЁвый. 
        """
        try:
            
            lCurs = self._cursor #.cursor()
            paramsObj = self.splitAttributes()
            listSet = map(lambda x, y: str(x) + " = '" + str(y) + "'", paramsObj.listAttrNames, paramsObj.listAttrValues)
            strSet =  ", ".join(listSet)
            sqlStr = "UPDATE "+ self._tabName +" SET " + strSet + " WHERE " + whereSection
            logging.info(' update:: sqlStr = ' + sqlStr)
            lCurs.execute(sqlStr)
            self.saverevision(autorId, 'U')

#             self.commit()
        except psycopg2.Error as error:
            logging.error(' update exception:: ' + str (error) )
            logging.error(' update exception:: sqlStr = ' + sqlStr )
            lCurs.rollback()
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
            users.author_id,  
            users.author_login, 
            users.author_name, 
            users.author_role, 
            users.author_phon, 
            users.author_email, 
            users.author_external 
        FROM users 
        WHERE (author_login =  "login" OR author_email =  "login" ) 
        AND author_pass =  "$2b$12$.b9454ab5a22859b68bb4uvIvIvpREbnd9t2DJ7rqm1bwB/PrsH0." 
        
              
        """
        try:
#             logging.info(' select:: addTables = ' + str(addTables))
            _loDb = self.cursor()
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

            _loDb.execute(sqlStr)
            sourse = _loDb.fetchall()
            logging.info('select:: list:: sourse = ' + str (sourse) )
            outListObj = self.dict2obj(sourse)    
 

            return outListObj

        except psycopg2.Error as error:
            logging.error(' select exception:: sqlStr = ' + sqlStr )
            _loDb.rollback()
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
#         objDict = self.__dict__
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
        out.strListAttrNames = ", ".join(listAttrNames)
        out.strListAttrValues = "'" + "', '".join(map(str,listAttrValues)) + "'"   
#         out.strListAttrValues = "'" + "', '".join(listAttrValues) + "'"   
        return out


 
    def dict2obj(self, dictSou):
        """
        преобразовать словарь (допустим, кортеж данных из селекта) в объект  
        """ 
        oList = []
        for row in dictSou:
#             logging.info(' dict2obj:: row = ' + str(row))
#             logging.info(' dict2obj:: type(row) = ' + str(type(row)))
            rowDict = dict(row)
#             logging.info(' dict2obj:: rowDict = ' + str(rowDict))
            oneObj = self.__class__()
            for key in rowDict.items(): #.__getattribute__(name):
#                 logging.info(' dict2obj:: key = ' + str(key))
                oneObj.__setattr__(key[0], key[1])
            oList.append(oneObj)
                
        return oList



    def __str__(self): 
        attribList = self.splitAttributes()
        className = str(self.__class__)
        itemsList = map(lambda x, y: ' "' + str(x) + '"' + ': "' + str(y) + '" ', attribList.listAttrNames, attribList.listAttrValues) 
        objValuesNameList = '\n'+ className + ': { \n\t' + ', \n\t'.join(itemsList) + '\n}'
        return objValuesNameList


##############################################
# Набор методов для  работы с Ревизиями! 
# - добавит ревизию 
# - получить список ревизий
# - получить оду ревизию...
# - узнать является ли набор данных уникальным (не похожим на текущее значение данных - значит, у нас возможны циклы!!!!!)

    def saveRevision(self, autorId, operationFlag, mainPrimaryObj, revisions_sha_hash):
        """
        сохранение ревизии для данных.
        при сохранении ревизии стоит (наверное) делать так:
        - сказать всем ревизиям, что они устарели (сделать флаг "О")
        - попытаться добавить ревизию (с флагом "А") 
        - если не получилось, то на ревизии с тем, актуальным ХЕШЕМ поставить фла "А"
        
        mainPrimaryObj = {primaryName: 'article_id', primaryValue: 123 }
         
        INSERT INTO distributors (did, dname)
        VALUES (5, 'Gizmo Transglobal')
        ON CONFLICT (did) DO UPDATE SET dname = EXCLUDED.dname;
            
        """
        paramsObj = self.splitAttributes()
# во тут надо добавить араметры ревизии в инсерт!!
#   actual_flag revision_data_type NOT NULL,
#   revision_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
#   revision_author_id int NOT NULL references authors(author_id),

        try:
            _loDb = self.cursor()
            _loDb.begin()
    
            # Все ревизии ЭТОЙ записи - устарели!!!! - проабдейтим список ревизий
            sqlStr = "UPDATE revisions_" + self._tabName + "SET revision_actual_flag = 'O' WHERE " +\
                     mainPrimaryObj.primaryName + " = "  + mainPrimaryObj.primaryValue
            _loDb.execute(sqlStr)

            # Теперь можно записать новые данные  в ревизии.    
            paramsObj.strListAttrNames += ', revision_actual_flag, revision_author_id,  operation_flag, revisions_sha_hash '
            paramsObj.strListAttrValues += ", 'A', " +  str(autorId) + ", '" + operationFlag + "',  '" + revisions_sha_hash + "' "
    
            sqlStr = "INSERT INTO revisions_" + self._tabName +" ( " + paramsObj.strListAttrNames + ") VALUES " +\
                    "( " + paramsObj.strListAttrValues + " ) " + \
                    " ON CONFLICT (revisions_sha_hash) DO UPDATE SET revision_actual_flag = 'A'; "
            logging.info(' insert:: sqlStr = ' + sqlStr)
            _loDb.execute(sqlStr)

            _loDb.commit()
        except psycopg2.Error as error:
            logging.error(' update exception:: ' + str (error) )
            logging.error(' update exception:: sqlStr = ' + sqlStr )
            _loDb.rollback()
            raise err.WikiException(error)



    def selectRevisions(self, 
               selectStr = '', # строка - чего хотим получить из селекта
               addTables = '',  # строка - список ДОПОЛНИТЕЛЬНЫХ таблиц (основную таблизу для объекта указываем при инициализации) 
               anyParams = {} #  все остальные секции селекта
               ):
        """
        сделать базовый селект, для работы с ревизиями,
         - добавляем к базовым данным оболочку "чисто ревизий" :-) 
         и поом уже вызывать ...
        
        """
        
        if addTables != '':  addTables += ", " 
        addTables += "revisions_" + self._tabName + ' rev '

        if selectStr != '' : selectStr += ', ' 
        selectStr += ' rev.operation_flag, EXTRACT(EPOCH FROM rev.revision_date) AS revision_date, '
        selectStr += ' author_name AS rev_author_name, author_surname AS rev_author_surname '
        
        strAddJoin = ' LEFT JOIN authors ON authors.author_id = rev.revision_author_id '
        
        return self.select(
                                selectStr,
                                addTables,
                                   { 
                               'joinStr': str(anyParams.get('joinStr')) + strAddJoin,
                               'whereStr': str(anyParams.get('joinStr'))
                                }
                               )

        
        def IsUniqueRevision(self, titleHash, annotationHash, textHash):
            """
            проверить, является ли данная ревизия уникальной 
            - может поменятся все, 
            - может - заглавие
            - может - аннотация
            - может текст
            """
            isUniqueRez = self.select(
                       ' revisions.text_sha_hash, revAnnotation.annotation_sha_hash, revTitle.title_sha_hash',
                       'revisions revTitle, revisions revAnnotation',
                           { 
                       'whereStr': " ( revTitle.title_sha_hash = '"+ titleHash + "' " +
                                    " OR revAnnotation.annotation_sha_hash = '"+ annotationHash + "' " +
                                    " OR revisions.text_sha_hash = '" + textHash  + "' ) " ,             # строка набор условий для выбора строк
                        }
                       )
            
            return isUniqueRez






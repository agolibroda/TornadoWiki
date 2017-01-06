#!/usr/bin/env python
#
# Copyright 2016 Alec Goliboda
#
# group.py

from __future__ import print_function

import logging
import json

import zlib
# import markdown
from datetime import datetime


import tornado.options
# import pymysql

import hashlib
import base64
        
from _overlapped import NULL

##############
import config


from . import Model
from .. import WikiException 

from core.models.template   import Template

from ..constants.data_base import * 


class Gpoup(Model):
    """
    модель - для Группы
    внутри будут:
    - список участников
    - библиотека
    
    выдавать будет 
    - список всех групп
    - одну группу (полностью?) может и не надо. 
    - создавать группы
    - "удалять группы" - о... нужен флаг - "группа удалена"!!!!!
    
    - добавлять (удаять) участников в группу
    - показывать список участников
    - добавлять (удалять) статьи в библиотеку
    - показывать список статей в библиотеке группы.
    
    Видимость групп (group_status) 
    - публичная - 'pbl'
    - закрытая - 'shut'
    
    """
    
    def __init__(self, group_title = '', group_annotation = '', group_status = 'pbl'):
        Model.__init__(self, 'groups')   

        self.group_id = 0
        self.author_id = 0
        self.group_title = group_title
        self.group_annotation = group_annotation
        self.group_status = group_status
        self.group_create_date = datetime.now()
        
        
    class Member(Model):
        def __init__(self):        
            Model.__init__(self, 'members')   
            self.group_id = 0
            self.author_id = 0
            self.member_role_type = 'M'
            
        def save(self, author_id ):

            try:
                self.insert()
            except Exception as e:
                logging.info( 'Member Save:: Exception as e = ' + str(e))

            operationFlag = 'I'

            mainPrimaryObj = {'primaryName': 'group_id', 'primaryValue': self.group_id }
            revisions_sha_hash_sou =  str(self.group_id) + str(self.author_id) + self.member_role_type 
            logging.info(' save:: mainPrimaryObj = ' + str(mainPrimaryObj))
            self.saveRevision(author_id, operationFlag, mainPrimaryObj, revisions_sha_hash_sou)


    class Library(Model):
        def __init__(self):        
            Model.__init__(self, 'librarys')   
            self.group_id = 0
            self.article_id = 0
            self.library_permission_type = 'W'

        def save(self, author_id):

            try:
                self.insert()
            except Exception as e:
                logging.info( 'Member Save:: Exception as e = ' + str(e))

            operationFlag = 'I'

            mainPrimaryObj = {'primaryName': 'group_id', 'primaryValue': self.group_id }
            revisions_sha_hash_sou =  str(self.group_id) + str(self.author_id) + self.member_role_type 
            logging.info(' save:: mainPrimaryObj = ' + str(mainPrimaryObj))
            self.saveRevision(author_id, operationFlag, mainPrimaryObj, revisions_sha_hash_sou)


    def get(self, group_id):
        """
        загрузить ОДНО значение - по ИД группы
        """
        resList = self.select(
                    'group_id,  group_title, group_annotation,  group_status, floor(EXTRACT(EPOCH FROM group_create_date)) AS group_create_date, ' + 
                    ' author_name, author_surname ' , # строка - чего хотим получить из селекта
                    ' authors ', #'authors',  # строка - список таблиц 
                    {
                     'whereStr': " groups.author_id = authors.author_id AND  groups.group_id = " + str(group_id)
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

    def list(self ):
        """
        загрузить список всех групп
        
        """
        resList = self.select(
                    'group_id,  group_title, group_annotation,  group_status, floor(EXTRACT(EPOCH FROM group_create_date)) AS group_create_date ' + 
                    ' author_name, author_surname ' , # строка - чего хотим получить из селекта
                    ' authors ', #'authors',  # строка - список таблиц 
                    {
                     'whereStr': " groups.author_id = authors.author_id "
                     } #  все остальные секции селекта
                    )
#         logging.info('Author:: get:: resList = ')
#         logging.info(resList)
        return resList
        

        
    def grouplistForAutor(self, author_id):
        """
        Получить список групп для одного автора - все руппы, которые АВТОР создал, 
        и в которых АВТОР является АДМИНОМ
        у, походу, инттереснее плучитьвсе группы АВТОРА - и где автор "Админ" и "учасник" 
        а авторство в группе ... ну, не знаю. :-)
        
        """
        resList = self.select(
                    'group_id,  group_title, group_annotation,  group_status, floor(EXTRACT(EPOCH FROM group_create_date)) AS group_create_date, ' + 
                    ' author_name, author_surname, groups.member_role_type ' , # строка - чего хотим получить из селекта
                    ' authors, members ', #'authors',  # строка - список таблиц 
                    {
                     'whereStr': " members.author_id = authors.author_id AND  group_id = " + str(author_id) +
                     " AND members.group_id = groups.group_id "
                     } #  все остальные секции селекта
                    )

        return resList
    
    
    def save(self, author_id ):
        """
        сщхранить группу, 
        пользователя, который создал группу надо воткнуть не только в авторы группы,
        но, и в "members" да еще и АДМИНОМ!!!
        
        """

        logging.info(' save:: before SAVE = ' + str(self)) 
               
        if self.group_id == 0:
            self.author_id = author_id
            self.group_create_date = datetime.now()
            self.group_id = self.insert('group_id')
            operationFlag = 'I'
        else:
            del(  self.group_create_date) # =  datetime.fromtimestamp(int(self.group_create_date))
            del(  self.author_id) # = self.author_id
#             self.group_create_date = datetime.now()
            self.update('group_id = ' + str(self.group_id))
            operationFlag = 'U'
            
        mainPrimaryObj = {'primaryName': 'group_id', 'primaryValue': self.group_id }
        revisions_sha_hash_sou = self.group_title + self.group_annotation + self.group_status
        
        logging.info(' save:: mainPrimaryObj = ' + str(mainPrimaryObj))
        self.saveRevision(author_id, operationFlag, mainPrimaryObj, revisions_sha_hash_sou)
        # теперь сохранить автора группы как ее админа.

        if operationFlag == 'I':
            memberControl = self.Member()
            memberControl.author_id = author_id
            memberControl.group_id = self.group_id
            memberControl.member_role_type = 'A'
            memberControl.save(author_id)
        
        
        return True

    
    
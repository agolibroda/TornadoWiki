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
        
# from _overlapped import NULL

##############
import config


from . import Model
from .. import WikiException 

# from core.models.template   import Template

from ..constants.data_base import * 


class Group(Model):
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
#         self.author_id = 0
        self.group_title = group_title
        self.group_annotation = group_annotation
        self.group_status = group_status
#         self.group_create_date = datetime.now()
        
        
    class Member(Model):
        def __init__(self):        
            Model.__init__(self, 'members')   
            self.group_id = 0
            self.author_id = 0
            self.member_role_type = 'M'
            
        def save(self, author_id ):

            operationFlag = 'I'

            mainPrimaryObj = {'group_id': self.group_id, 'author_id': self.author_id }
            revisions_sha_hash_sou =  str(self.group_id) + str(self.author_id) + self.member_role_type 
            logging.info(' Member save:: self = ' + str(self))
            Model.save(self, author_id, operationFlag, mainPrimaryObj, revisions_sha_hash_sou)


        def getGroupMembersleList(self, groupId):
            """
            Получить список всех соучастников одной группы
            
            """

            getRez = self.select(
                    'authors.author_id,  author_login, author_name, author_surname, author_role, author_phon, author_email ',
                    'authors',
                        {
                    'whereStr': " members.author_id = authors.author_id  AND " +\
                    " members.actual_flag = 'A' AND authors.actual_flag = 'A' AND "
                    " members.group_id = " + str(groupId) , # строка набор условий для выбора строк
                    'orderStr': ' author_name, author_surname ', # строка порядок строк
                                     }
                                    )

# 'whereStr': " groups.author_id = authors.author_id AND  groups.group_id = " + str(group_id)            
        
            logging.info( 'getGroupMembersleList:: getRez = ' + str(getRez))
            if len(getRez) == 0:
    #             raise WikiException( ARTICLE_NOT_FOUND )
               return []
             
#             for oneObj in getRez:
#                 oneObj.article_title = base64.b64decode(oneObj.article_title).decode(encoding='UTF-8')
#                 oneObj.article_link = base64.b64decode(oneObj.article_link).decode(encoding='UTF-8')
#     #              articleTitle = oneObj.article_title.strip().strip(" \t\n")
#     #              oneObj.article_link  =  articleTitle.lower().replace(' ','_')
#                 oneObj.article_annotation =  base64.b64decode(oneObj.article_annotation).decode(encoding='UTF-8')
#     #              logging.info( 'list:: After oneArt = ' + str(oneObj))
#         
            return getRez


    class Library(Model):
        
        def __init__(self, group_id = 0, article_id=0, library_permission_type = 'W' ):        
            Model.__init__(self, 'librarys')   
            self.group_id = group_id
            self.article_id = article_id
            self.library_permission_type = library_permission_type

        def save(self, author_id):

            operationFlag = 'I'

            mainPrimaryObj = {'group_id': self.group_id, 'article_id': self.article_id }
            revisions_sha_hash_sou =  str(self.group_id) + str(self.article_id) + self.library_permission_type 
            logging.info(' Library save:: self = ' + str(self))
            Model.save(self, author_id, operationFlag, mainPrimaryObj, revisions_sha_hash_sou)


        def getGroupArticleList(self, groupId):
            """
            Получить список всех статей одной группы
            
            """

            getRez = self.select(
                    ' articles.article_id, articles.article_title, articles.article_link, ' +
                    ' articles.article_annotation, articles.article_category_id, ' + 
                    ' articles.article_template_id, ' +
                    ' null AS group_title, null AS group_annotation,  null AS group_id ',
                    'articles',
                        {
                    'whereStr': " librarys.article_id = articles.article_id AND " +\
                    " articles.actual_flag = 'A' AND librarys.actual_flag = 'A' AND "
                    " librarys.group_id = " + str(groupId) , # строка набор условий для выбора строк
                    'orderStr': ' articles.article_id ', # строка порядок строк
                                     }
                                    )

# 'whereStr': " groups.author_id = authors.author_id AND  groups.group_id = " + str(group_id)            
            for item in getRez:
                logging.info( 'getGroupArticleList:: getRez = ' + str(item))
            
            if len(getRez) == 0:
    #             raise WikiException( ARTICLE_NOT_FOUND )
               return []
             
            return getRez
    


    def get(self, group_id):
        """
        загрузить ОДНО значение - по ИД группы
        """
        resList = self.select(
                    'group_id,  group_title, group_annotation ' , # строка - чего хотим получить из селекта
                    '', #'authors',  # строка - список таблиц 
                    {
                     'whereStr': " groups.actual_flag = 'A' AND  groups.group_id = " + str(group_id)
                     } #  все остальные секции селекта
                    )
        for item in resList:
            logging.info('Author:: get:: resList = ' + str(item))
            
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
                    'group_id,  group_title, group_annotation,  group_status  ' , # строка - чего хотим получить из селекта
                    '', #'authors',  # строка - список таблиц 
                    {
                     'whereStr': " groups.actual_flag = 'A' "
                     } #  все остальные секции селекта
                    )
#         logging.info('Author:: get:: resList = ')
#         logging.info(resList)
        return resList
        

        
    def grouplistForAutor(self, author_id):
        """
        Получить список групп для одного автора - все руппы, которые АВТОР создал, 
        и в которых АВТОР является участником
       
        вот тут возможно, надо будет все поправить - 
        и показывать только ПАБЛИК группы, и/или приватные группы, 
        в которых участвуют оба  - и зритель, и автор 
        
        """
        try:
            resList = self.select(
                        ' DISTINCT groups.group_id,  groups.group_title, groups.group_annotation,  groups.group_status, ' + 
                        ' members.member_role_type ' , # строка - чего хотим получить из селекта
                        '  members', #'authors',  # строка - список таблиц 
                        {
                         'whereStr': " groups.actual_flag = 'A' AND members.author_id = " + str(author_id) + \
                         " AND  members.group_id = groups.group_id ",
                         'orderStr': '  groups.group_title ' 
                         } #  все остальные секции селекта
                        )
            
#             logging.info( 'grouplistForAutor:: resList =  ' + str(resList))
            return resList
        except Exception as e:        
#         except WikiException as e:   
#             WikiException( ARTICLE_NOT_FOUND )
            logging.info( 'grouplistForAutor::Have ERROR!!!  ' + str(e))
            if not article: raise tornado.web.HTTPError(404)
            else: return (article, [])
     
    
    def getGroupArticleList(self, groupId):
        """
        Получить список всех статей одной группы
        
        """
        libControl = self.Library ()
        return libControl.getGroupArticleList( groupId)


    def getGroupMembersleList(self, groupId):
        """
        Получить список всех Участников одной группы
        
        """
        memberControl = self.Member ()
        return memberControl.getGroupMembersleList( groupId)

    
    def save(self, author_id ):
        """
        сщхранить группу, 
        пользователя, который создал группу надо воткнуть не только в авторы группы,
        но, и в "members" да еще и АДМИНОМ!!!
        
        """

        logging.info(' save:: before SAVE = ' + str(self)) 
               
        if self.group_id == 0:
#             self.group_create_date = datetime.now()
            operationFlag = 'I'
        else:
            operationFlag = 'U'
        
        self.begin()    
        mainPrimaryObj = {'group_id': self.group_id }
        revisions_sha_hash_sou = self.group_title + self.group_annotation + self.group_status
        
        logging.info(' save:: mainPrimaryObj = ' + str(mainPrimaryObj))
        self.group_id =  Model.save(self, author_id, operationFlag, mainPrimaryObj, revisions_sha_hash_sou, 'group_id')
        # теперь сохранить автора группы как ее админа.

        if operationFlag == 'I':
            memberControl = self.Member()
            memberControl.author_id = author_id
            memberControl.group_id = self.group_id
            memberControl.member_role_type = 'A'
            memberControl.save(author_id)
        
        self.commit()
        return True


    def librarySave(self, author_id = 0, group_id = 0, article_id=0, library_permission_type = 'W'):
        """
        Добавить статью к группе 
        
        """
        libControl = self.Library (group_id, article_id, library_permission_type)
        libControl.save(author_id)

    
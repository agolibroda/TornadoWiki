#!/usr/bin/env python
#
# Copyright 2015 Alec Goliboda
#
# article.py


from __future__ import print_function

import logging
import json

import zlib
# import markdown

import tornado.options
# import pymysql

import hashlib
import base64
        
from _overlapped import NULL

##############
import config


from . import Model
from .. import WikiException 

# import core.models.template
# from .template import Template
# from . import Template
from core.models.template   import Template

from core.WikiException     import *


from ..constants.data_base import * 


# def parse_utf8(self, bytes, length_size):
# 
#     length = bytes2int(bytes[0:length_size])
#     value = ''.join(['%c' % b for b in bytes[length_size:length_size+length]])
#     return value


class Article(Model):
    """
    статья  - основной объект данных для системы;
    
    иммет 
    - автора
    - название 
    - текст
    
    название и текст могут менятся. 
     
    articles - хранилище ВСЕХ статей в системе.
    revisions_articles - хранилище всех ревиий. 
    
    статья Это:
    - заглавие
    - текст стаьи (актуальный)
    - автор 
    - дата создания
    
    - категория статьи (article_category_id)
        информационная    inf - тут ИД статьи из списка!!!!
        термин            trm
        навигационная     nvg
        шабон             tpl
    - шабон статьи (article_template_id)
        по ИД шаблона выбирается шаблон, который оформляет текущий текст статьи  
    - права доступа (article_permissions)
        публичкая (свободный доступ)    pbl
        групповая (права на статью есть только у группы) grp
        персональная (исключительно авторская)    sol (solo)
    
        
    - текст хранится в виде, готовом для публикации (в хтмл-ке)
    - список ревизий названия статьи и текста 
        у каждой ревизии есть дата и автор ревизии
    
    при сохранении статьи
    1. подготовить текст 
    2 сохранить.
     
    получить список статей 
    - выбираем данные из "articles" - 
    
    получить одну статью 
    - по одному из имен (старых - новых не важно) 
    выбираем данные из  "articles" 
    данные ревизий берутся  по ХЕШУ-ам в таблицах "titles", "annotations", "texts"
    
    получить историю статьи 
    - по  ИД (одному из имен) выбрать все версии статьи из "revisions"
    
    """
 
    def __init__ (self, id=0, title = ''): 
#         logging.info('article:: __init__')

        Model.__init__(self, 'articles')   
        self.article_id = id # эти параметры прилетают из формы редактирования
        self.author_id = 0;
        self.article_title = title # эти параметры прилетают из формы редактирования
        self.article_annotation = '' # Это аннотация статьи!!!!!
        self.article_source = '' # эти параметры прилетают из формы редактирования
        self.article_category_id = config.options.info_page_categofy_id # категория страницы (служебные?) 'inf','trm','nvg','tpl'
        self.article_template_id = config.options.main_info_template
        self.article_permissions = 'pbl'
#         self.article_link = '' 

        

    def save(self, author_id, templateDir):
        """
        сохранить данные.
        2.1 поменятся могут:
            - название статьи
            - аннотация 
            - текст 
        2.1.1 надо проверить, является ли эта троица УНИКАЛЬНОЙ - 
        не важно ЧТО конкретно, может поменяться что - то одно, НО, 155 копий одного и тогоже нам не нужно (подозреваю!)
        значит, делает длинную строку, и берем от нее ХЭШ 
        смотрим по таблице ревизий - есть ли точно такое же, если сть, то 
        одаем автору ошибку, если все нормално, тогда записываем статью, и записываем ревизию.
        2.2.1 поменяем запись в "article"
        2.2.2 добавим новую запись в "revisions_articles"  
        
        """

# categories 
# Это новая таблица  - все категории, которые только озможны, и пока там  
# вот такие категрии (служебные?) 'inf','trm','nvg','tpl'

#         artModel.article_id = self.get_argument("id", 0)
#         artModel.article_title = self.get_argument("article_title")
#         artModel.article_annotation = self.get_argument("article_annotation")
#         artModel.article_source = self.get_argument("article_source")


        self.author_id = author_id
       
#         self.article_id = self.get_argument("id", 0)
#         self.article_category_id = self.get_argument("category_id", 0)
#         self.article_template_id = self.get_argument("template_id", 0)
#         self.article_permissions = self.get_argument("permissions", '')
#         
#         article_title = self.get_argument("title", '')
#         article_annotation = self.get_argument("annotation", '')
#         article_source = self.get_argument("sourse", '')

        article_title = self.article_title.strip().strip(" \t\n")
        article_link = article_title.lower().replace(' ','_')
        article_link = article_link.replace('__','_')

        article_title = base64.b64encode(tornado.escape.utf8(article_title)).decode(encoding='UTF-8')
        article_link = base64.b64encode(tornado.escape.utf8(article_link)).decode(encoding='UTF-8')
        article_annotation = base64.b64encode(tornado.escape.utf8(self.article_annotation)).decode(encoding='UTF-8')    
        article_source = base64.b64encode(
                                    zlib.compress(
                                        tornado.escape.utf8(self.article_source)
                                                )
                                                    ).decode(encoding='UTF-8')
        

        self.article_title = article_title
        self.article_link = article_link
        self.article_annotation = article_annotation  
        self.article_source = article_source
#         base64.b64encode(tornado.escape.utf8(article_source)).decode(encoding='UTF-8') 

#         
# вот тут по - идее, надо начать трансакцию... 
# - почитать про трансакции в постгрисе. 
# 
# BEGIN;
# UPDATE accounts SET balance = balance + 100.00 WHERE acctnum = 12345;
# UPDATE accounts SET balance = balance - 100.00 WHERE acctnum = 7534;
# COMMIT;
#             self.rollback()


        self.begin()

        logging.info( 'article Before Save : self.article_id = ' + str(self) )
        
        try:
        
            if int(self.article_id) == 0:
                self.article_id = self.insert('article_id')
                operationFlag = 'I'
                        
            else:
                self.update('article_id = ' + str (self.article_id))
                operationFlag = 'U'
    
            self.commit()
        
# вот после всего надо сохранить шаблон в шаблоновую директорию... 
            logging.info( 'save:: save self.article_category_id = ' + str(self.article_category_id))
            logging.info( 'save:: save 2 self.article_category_id = ' + str(int(self.article_category_id)))
            logging.info( 'save:: save config.options.tpl_categofy_id = ' + str(config.options.tpl_categofy_id))
            logging.info( 'save:: save 2 config.options.tpl_categofy_id = ' + str(int(config.options.tpl_categofy_id)))
            logging.info( 'save:: save self.article_id = ' + str(self.article_id))
                
            if int(self.article_category_id) == int(config.options.tpl_categofy_id):
                logging.info( 'save:: save Template! = ' )
                 
                wrkTpl = Template()
                wrkTpl.save(self.article_id, htmlTextOut, templateDir)
            
            
                
            revisions_sha_hash = hashlib.sha256(
                               tornado.escape.utf8(article_title + article_annotation + article_source)
                               ).hexdigest()   #.decode(encoding='UTF-8')

            mainPrimaryObj = {'primaryName': 'article_id', 'primaryValue': self.article_id }
            self.saveRevision(self.author_id, operationFlag, mainPrimaryObj, revisions_sha_hash)


        except Exception as e:
            logging.info( 'Save:: Exception as et = ' + str(e))
            self.rollback()
             
        self.article_link = titleLink 
        logging.info( 'save:: save self.article_link! = ' + self.article_link )
                
        return self 
         

# где - то после сохранения данных, должна быть сохранена и ревизия, причем, в единой трансакции!!!!
#   -- вот, такое изменение уже есть, и нефок его заново запихивать!
#   revisions_sha_hash character varying(66) NOT NULL, 
# 
# процедура - сохранить трансакцию!!!!!


    def get(self, articleLink):
         """
         получить статью по названию (одну) - функция для пердставления данных (!!!) 
         получить ОЛЬКО опубликованный текст  (активную статью) - для редактирования получаем статью иным образом! 
    
         - по одному из имен (старых - новых не важно) 
         выбираем данные из "article" и "articles" берем как ХТМЛ, так и РТФ ну и активный тайтл (ил "articles")
         имя ищем по ХЕШУ в таблице "titles"
         
         """
         logging.info( 'Article ::: get articleLink  = ' + str(articleLink))
    
         article_link = base64.b64encode(tornado.escape.utf8(articleLink)).decode(encoding='UTF-8')

#          articleLink = hashlib.sha256(
#                                      tornado.escape.utf8(articleLink)
#                                      ).hexdigest()  #.decode(encoding='UTF-8')
#     
         getRez = self.select(
                                'articles.article_id, articles.article_title, articles.article_link, ' + 
                                'articles.article_annotation,  articles.article_source, articles.article_category_id, articles.author_id, articles.article_template_id ',
                                ' revisions_articles lfind ',
                                    {
                                'whereStr': " articles.article_id = lfind.article_id " +
                                             " AND lfind.article_link = '" + article_link  + "' " , # строка набор условий для выбора строк
                                 }
                                )
    
         if len(getRez) == 0:
            raise WikiException( ARTICLE_NOT_FOUND )
         elif len(getRez) == 1:   
            outArt = getRez[0]
            outArt.article_title = base64.b64decode(outArt.article_title).decode(encoding='UTF-8')
            outArt.article_link = base64.b64decode(outArt.article_link).decode(encoding='UTF-8')
            outArt.article_annotation = base64.b64decode(outArt.article_annotation).decode(encoding='UTF-8')
            decodeText =  base64.b64decode(outArt.article_source) #.decode(encoding='UTF-8')
            outArt.article_source = zlib.decompress(decodeText)  #.decode('UTF-8')    

            logging.info( 'get outArt = ' + str(outArt))

#        textControl.text_html = base64.b64encode(
#                                     zlib.compress(
#                                         tornado.escape.utf8(self.article_html)
#                                                 )
#                                                     ).decode(encoding='UTF-8')
#      
            return outArt


    def getById(self, articleId):
         """
         получить статью по ID (одну) - функция для пердставления данных (!!!) 
         получить ОЛЬКО опубликованный текст  (активную статью) - для редактирования получаем статью иным образом! 
    
         """
         logging.info( 'Article ::: getById articleId  = ' + str(articleId))
    
         getRez = self.select(
                                'articles.article_id, articles.article_title, articles.article_link, '+
                                'articles.article_annotation,  articles.article_source, articles.article_category_id, '+ 
                                'articles.author_id, articles.article_template_id',
                                '',
                                    {
                                'whereStr': ' articles.article_id = ' + str(articleId)  ,
                                 }
                                )
    
         if len(getRez) == 0:
            raise WikiException( ARTICLE_NOT_FOUND )
         elif len(getRez) == 1:   
#              logging.info( ' getById getRez = ' + str(getRez[0]))
             outArt = getRez[0]
             outArt.article_title = base64.b64decode(outArt.article_title).decode(encoding='UTF-8')
             outArt.article_link = base64.b64decode(outArt.article_link).decode(encoding='UTF-8')
             outArt.article_annotation = base64.b64decode(outArt.article_annotation).decode(encoding='UTF-8')
             outArt.article_source =  base64.b64decode(outArt.article_source).decode(encoding='UTF-8')
    #             logging.info( 'outArt.article_source = ' + str(outArt.article_source))
    
#              articleTitle = outArt.article_title.strip().strip(" \t\n")
#              outArt.article_link =  articleTitle.lower().replace(' ','_')
             
#              logging.info( ' getById outArt = ' + str(outArt))
             return outArt



    def getByUsingHash(self, hash):
         """
         получить статью (ВЕРСИЮ) по hash (одну) 
         а вот что показать? 
         ну, походу, все, из ТОЙ версии, которую заказал пользователь!!! 
    
         """
         logging.info( 'Article ::: getById articleId  = ' + str(articleId))
    
         getRez = self.select(
                                'articles.article_id, articles.article_title, articles.article_link, '+
                                'articles.article_annotation,  articles.article_source, articles.article_category_id, '+ 
                                'articles.author_id, articles.article_template_id',
                                '',
                                    {
                                'whereStr': ' articles.article_id = ' + str(hash)  ,
                                 }
                                )
    
         if len(getRez) == 0:
            raise WikiException( ARTICLE_NOT_FOUND )
         elif len(getRez) == 1:   
#              logging.info( ' getById getRez = ' + str(getRez[0]))
             outArt = getRez[0]
             outArt.article_title = base64.b64decode(outArt.article_title).decode(encoding='UTF-8')
             outArt.article_link = base64.b64decode(outArt.article_link).decode(encoding='UTF-8')
             outArt.article_annotation = base64.b64decode(outArt.article_annotation).decode(encoding='UTF-8')
             outArt.article_source =  base64.b64decode(outArt.article_source).decode(encoding='UTF-8')
    #             logging.info( 'outArt.article_source = ' + str(outArt.article_source))
    
#              articleTitle = outArt.article_title.strip().strip(" \t\n")
#              outArt.article_link =  articleTitle.lower().replace(' ','_')
             
#              logging.info( ' getById outArt = ' + str(outArt))
             return outArt

    
    def list(self, categoryId = 0):
         """
         получить список статей
         упорядочивать потом будем
    
         получить список статей 
         - выбираем данные из "articles" - получить при этом АКТАЛЬНЫЕ ИД ревизий!
                 
         """
    
         categoryStr = '';
         if categoryId > 0 :
             categoryStr = ' articles.article_category_id = ' + str(categoryId)
             
         getRez = self.select(
    #                                'articles.article_id, FROM_BASE64(articles.article_title),  FROM_BASE64(articles.article_source) ',
                                'articles.article_id, articles.article_title, articles.article_link, ' +
                                'articles.article_annotation, articles.article_category_id, articles.author_id, articles.article_template_id ',
                                '',
                                    {
                                'whereStr': categoryStr, # строка набор условий для выбора строк
                                'orderStr': ' articles.article_title ', # строка порядок строк
    #                                'orderStr': 'FROM_BASE64( articles.article_title )', # строка порядок строк
                                 }
                                )
    
         logging.info( 'list:: getRez = ' + str(getRez))
         if len(getRez) == 0:
#             raise WikiException( ARTICLE_NOT_FOUND )
            return []
         
         for oneObj in getRez:
             oneObj.article_title = base64.b64decode(oneObj.article_title).decode(encoding='UTF-8')
             oneObj.article_link = base64.b64decode(oneObj.article_link).decode(encoding='UTF-8')
#              articleTitle = oneObj.article_title.strip().strip(" \t\n")
#              oneObj.article_link  =  articleTitle.lower().replace(' ','_')
             oneObj.article_annotation =  base64.b64decode(oneObj.article_annotation).decode(encoding='UTF-8')
#              logging.info( 'list:: After oneArt = ' + str(oneObj))
    
         return getRez
 
    def listByAutorId(self, authorId = 0):
         """
         получить список статей
         одного автор - все статьи, всех категорий!
    
         получить список статей 
         - выбираем данные из "articles" - получить при этом АКТАЛЬНЫЕ ИД ревизий!
                 
         """
    
         autorIdStr = '';
         if authorId > 0 :
             autorIdStr = ' articles.author_id  = ' + str(authorId)
             
         getRez = self.select(
    #                                'articles.article_id, FROM_BASE64(articles.article_title),  FROM_BASE64(articles.article_source) ',
                                'articles.article_id, articles.article_title, articles.article_link, ' +
                                'articles.article_annotation, articles.article_category_id, articles.author_id, articles.article_template_id ',
                                '',
                                    {
                                'whereStr': autorIdStr, # строка набор условий для выбора строк
                                'orderStr': ' articles.article_id ', # строка порядок строк
    #                                'orderStr': 'FROM_BASE64( articles.article_title )', # строка порядок строк
                                 }
                                )
    
         logging.info( 'list:: getRez = ' + str(getRez))
         if len(getRez) == 0:
#             raise WikiException( ARTICLE_NOT_FOUND )
            return []
         
         for oneObj in getRez:
             oneObj.article_title = base64.b64decode(oneObj.article_title).decode(encoding='UTF-8')
             oneObj.article_link = base64.b64decode(oneObj.article_link).decode(encoding='UTF-8')
#              articleTitle = oneObj.article_title.strip().strip(" \t\n")
#              oneObj.article_link  =  articleTitle.lower().replace(' ','_')
             oneObj.article_annotation =  base64.b64decode(oneObj.article_annotation).decode(encoding='UTF-8')
#              logging.info( 'list:: After oneArt = ' + str(oneObj))
    
         return getRez
   
    
    def get2Edit( self, articleId, revisionId ):
        """
        получить ОДНУ ревизию статьи        
        
        Это делаем для РЕДАКТИРОВНИЯ!!!
        
        """

        textColtrol = self.Text()
        return textColtrol.get2Edit( articleId, revisionId )


    def revisionsList(self, articleId):
        """
        получить список ревизий для одной статей
        упорядочивать по дате ревизии - в начале - самые последние
        Обязательно - автора!

        - выбираем данные из "revisions"  и "titles"  и "authors" 
        """
        pass
#         revControl = self.RevisionLoc()
#         return revControl.revisionsList(articleId)


    def IsUniqueRevision(self, titleHash, annotationHash, articleHash):
        """
        проверить, является ли данная ревизия уникальной 
        - может поменятся все, 
        - пожет - заглавие
        - может текст
        """
        revControl = self.RevisionLoc()
        return revControl.IsUniqueRevision(titleHash, annotationHash, articleHash)



    def getOneRevision ( self, articleId, revisionHash ):
        """
        получить ОДНУ ревизию статьи  
        у всякой ревизии есть ее уникальный Хуш!       
        для всякого типа данных известно, как этот Хеш создается, и знаит,
        по такому Хешу мохно поднять любую трансакцию!!!!
        
        Это делаем для РЕДАКТИРОВНИЯ!!!
        
        """

        getRez = self.select(
                               'texts.article_id, revisions.revision_id, texts.article_source, annotations.annotation_text, titles.title_text, ' +
                               ' EXTRACT(EPOCH FROM revisions.revision_date) AS revision_date,  revisions.author_id, revisions.revision_actual_flag, ' +
                               'articles.article_category_id, articles.article_template_id, articles.author_id ' ,
                               'revisions_articles, articles',
                                   {
                               'whereStr': "  texts.text_sha_hash =  revisions.text_sha_hash" +
                                            " AND titles.title_sha_hash = revisions.title_sha_hash " +
                                            " AND annotations.annotation_sha_hash = revisions.annotation_sha_hash " +
                                            " AND revisions.article_id = articles.article_id " +
                                            " AND revisions.revision_id = " + revisionId  + " " +
                                            " AND revisions.article_id = " + articleId  + " "  #### строка набор условий для выбора строк
                                }
                               )

        if len(getRez) == 0:
            raise WikiException( ARTICLE_NOT_FOUND )
        elif len(getRez) == 1:   
#             logging.info( 'getRez = ' + str(getRez[0]))
            outArt = getRez[0]
            outArt.article_title = base64.b64decode(outArt.title_text).decode(encoding='UTF-8')
            outArt.article_annotation = base64.b64decode(outArt.annotation_text).decode(encoding='UTF-8')
            decodeText =  base64.b64decode(outArt.article_source)
            outArt.article_source = zlib.decompress(decodeText).decode('UTF-8')    
#             logging.info( 'outArt.article_source = ' + str(outArt.article_source))

            articleTitle = outArt.article_title.strip().strip(" \t\n")
            outArt.article_link =  articleTitle.lower().replace(' ','_')
#                 self.article_link = titleText
            
            del(outArt.title_text) 
            del(outArt.text_html) 
            del(outArt.annotation_text) 

#                 logging.info( 'TEXT ::: get2Edit outArt  = ' + str(outArt))
             
            return outArt

 
 
#     def select(self, 
#                selectStr, # строка - чего хотим получить из селекта
#                addTables,  # строка - список ДОПОЛНИТЕЛЬНЫХ таблиц (основную таблизу для объекта указываем при инициализации) 
#                anyParams = {} #  все остальные секции селекта
#                ):
        
# вот тут надо добавить к списку того, что может придти из наследной модели :-)  
# "чисто" ревизные вещи - дату, автора, флаг 
# и уже в таком порядке все и выбирать... 
        
        def revisionsList(self, articleId):
            """
            получить список ревизий для одной статей
            упорядочивать по дате ревизии - в начале - самые последние
            Обязательно - автора!
    
    
            - выбираем данные из "texts"  и "annotations"  и "titles"  и "authors" 
            
            
            """
            getRez = self.select(
    #                                'articles.article_id, FROM_BASE64(articles.article_title),  FROM_BASE64(articles.article_source) ',
                                   ' EXTRACT(EPOCH FROM revisions.revision_date) AS revision_date, '+ 
                                   ' revisions_articles.article_id, revisions_articles.revisions_sha_hash, ' +
                                   ' revisions_articles.article_title, revisions_articles.article_annotation, ' +
                                   ' revisions_articles.author_id, authors.author_name, authors.author_surname ' +
                                   ' revisions_articles.revision_author_id, rev_author.author_name AS revision_author_name, rev_author.author_surname AS revision_author_surname',
                                   
                                   ' revisions_articles, authors, authors rev_author ',
                                   
                                       {
                                   'whereStr': ' revisions.author_id =  authors.author_id '  +
                                            ' AND revisions.revision_author_id =  rev_author.author_id '  +
                                            ' AND revisions.article_id =  ' + str(articleId), # строка набор условий для выбора строк
                                   'orderStr': ' revisions.revision_date DESC ', # строка порядок строк
    #                                'orderStr': 'FROM_BASE64( articles.article_title )', # строка порядок строк
                                    }
                                   )
    
            if len(getRez) == 0:
                raise WikiException( ARTICLE_NOT_FOUND )
            
            for oneObj in getRez:
    #             logging.info( 'list:: Before oneArt = ' + str(oneObj))
                
                oneObj.article_title = base64.b64decode(oneObj.title_text).decode(encoding='UTF-8')
                articleTitle = oneObj.article_title.strip().strip(" \t\n")
                oneObj.article_link =  articleTitle.lower().replace(' ','_')
#                 oneObj.article_source =  base64.b64decode(oneObj.article_source).decode(encoding='UTF-8')

#         logging.info( 'article:: revisionsList:::  str(len(getRez)) = ' + str(len(getRez)))
#         logging.info( 'article:: revisionsList:::  getRez = ' + str(getRez))
            return getRez









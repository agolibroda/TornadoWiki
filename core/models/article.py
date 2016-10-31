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
     
    articles - все версии всех статей лежат в этой таблице. 
    - одна статья  - один ИД - все изменения  - просто в смене флага. Каждый текст имеет уникальный ХЕШ
    - любые смены в "article_title" - сразу записываются как новый хеш в таблицу "titles"  
    поиск статьи по ее названию  (по любым старым названиям) делается по хешам в таблице  "titles"
    - актуальный текст сразу готовится к изданию, и помещается в таблицу "published"
    
    статья Это:
    - заглавие
    - текст стаьи (актуальный)
    
    - категория статьи (category_article_id)
        информационная    inf
        термин            trm
        навигационная     nvg
        шабон             tpl
    - шабон статьи (template)
        по ИД шаблона выбирается шаблон, который оформляет текущий текст статьи  
    - права доступа (permissions)
        публичкая (свободный доступ)    pbl
        групповая (права на статью есть только у группы) grp
        персональная (исключительно авторская)    sol (solo)
    
    наверное, поля (тип, шаблон, права) стоило бы разместить в таблице "published"
        
    - текст и название подготовленные для показа (в хтмл-ке)
    - список ревизий названия статьи и текста 
        у каждой ревизии есть дата и автор ревизии
    
    при сохранении статьи
    1. подготовить текст в ХТМЛ 
    2 сохранить.
    2.1 если текст новый
    2.1.1 добавим новый запись в "published" и получим новую ИД
    2.1.2 добавим новую запись в "articles" с флагом "А" 
        хеш делаем из суммы текста и заголовка статьи 
    2.1.3 добавим новую запись в "titles" - хешируем название статьи, и хеш добавляем в таблицу.
    - 
    2.2 если текст поменялся
    2.2.1 поменяем запись в "published"
    2.2.2 в "articles" для текущего ИД  поменяем все флаги на "N"
    2.2.3 добавим новую запись в "articles" с флагом "А"
        хеш делаем из суммы заголовка статьи и текста,  и, 
        если в статье (название+РТФ) ничего не поменялось, то сохранить мы не сможем.
    2.2.4 добавим новую запись в "titles" - хешируем название статьи, и хеш добавляем в таблицу. 
        если название менялось, то запись будет добавлена  
    2.3 в любом случае делается запись о новой ревизии "revisions". 
        (автор, хеш статьи, хеш заголовка, дата...)
    
    получить список статей 
    - выбираем данные из "published" - 
    
    получить одну статью 
    - по одному из имен (старых - новых не важно) 
    выбираем данные из "published" и "articles" берем как ХТМЛ, так и РТФ ну и активный тайтл (ил "articles")
    имя ищем по ХЕШУ в таблице "titles"
    
    получить историю статьи 
    - по  ИД (одному из имен) выбрать все версии статьи из "revisions"
    
    """

#########################################################################    
 
    class Text(Model):
        def __init__ (self): 
            Model.__init__(self, 'texts')   
            self.article_id = 0
            self.text_html = '' 
            self.text_sha_hash = ''

        def get2Edit( self, articleId, revisionId ):
            """
            получить ОДНУ ревизию статьи        
            
            Это делаем для РЕДАКТИРОВНИЯ!!!
            
            """
    
            getRez = self.select(
                                   'texts.article_id, revisions.revision_id, texts.text_html, annotations.annotation_text, titles.title_text, ' +
                                   ' EXTRACT(EPOCH FROM revisions.revision_date) AS revision_date,  revisions.user_id, revisions.revision_actual_flag, ' +
                                   'articles.category_article_id, articles.template ' ,
                                   'titles, revisions, annotations, articles',
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
                raise err.WikiException( ARTICLE_NOT_FOUND )
            elif len(getRez) == 1:   
    #             logging.info( 'getRez = ' + str(getRez[0]))
                outArt = getRez[0]
                outArt.article_title = base64.b64decode(outArt.title_text).decode(encoding='UTF-8')
                outArt.article_annotation = base64.b64decode(outArt.annotation_text).decode(encoding='UTF-8')
                decodeText =  base64.b64decode(outArt.text_html)
                outArt.article_html = zlib.decompress(decodeText).decode('UTF-8')    
    #             logging.info( 'outArt.article_html = ' + str(outArt.article_html))
    
                articleTitle = outArt.article_title.strip().strip(" \t\n")
                outArt.article_link =  articleTitle.lower().replace(' ','_')
#                 self.article_link = titleText
                
                del(outArt.title_text) 
                del(outArt.text_html) 
                del(outArt.annotation_text) 

#                 logging.info( 'TEXT ::: get2Edit outArt  = ' + str(outArt))
                 
                return outArt




    class Annotation(Model):
        """
        Это возможность работать и менять 
        "кракое описание страницы" 
        Это поле будет использоваться при прсмотре списка статей.... 
        ну при показе - редактировании, так то само-собой.
        """
        def __init__ (self): 
            Model.__init__(self, 'annotations')   
            self.article_id = 0
            self.annotation_text = ''
            self.annotation_sha_hash = ''


   
    class Title(Model):
        def __init__ (self): 
            Model.__init__(self, 'titles')   
            self.article_id = 0
            self.title_text = ''
            self.title_sha_hash = ''


    class RevisionLoc(Model):
        def __init__ (self): 
            Model.__init__(self, 'revisions')   
            self.revision_id = 0
            self.article_id = 0
            self.user_id = 0
# дата создания ревизии   
#             self.revision_date = 0
#             self.revision_actual_flag  = 'A'
            self.title_sha_hash = ''
            self.annotation_sha_hash = ''
            self.text_sha_hash = ''

        def revisionsList(self, articleId):
            """
            получить список ревизий для одной статей
            упорядочивать по дате ревизии - в начале - самые последние
            Обязательно - автора!
    
    
            - выбираем данные из "texts"  и "annotations"  и "titles"  и "users" 
            
            
            """
            getRez = self.select(
    #                                'articles.article_id, FROM_BASE64(articles.article_title),  FROM_BASE64(articles.article_html) ',
                                   ' EXTRACT(EPOCH FROM revisions.revision_date) AS revision_date, '+ 
                                   ' revisions.article_id, revisions.revision_id, ' +
                                   ' titles.title_text, annotations.annotation_text, ' +
                                   ' users.user_id, users.user_name ',
                                   ' titles, annotations, users ',
                                       {
                                   'whereStr': ' revisions.title_sha_hash = titles.title_sha_hash '  +
                                            ' AND revisions.annotation_sha_hash = annotations.annotation_sha_hash '  +
                                            ' AND revisions.user_id =  users.user_id '  +
                                            ' AND revisions.article_id =  ' + str(articleId), # строка набор условий для выбора строк
                                   'orderStr': ' revisions.revision_date DESC ', # строка порядок строк
    #                                'orderStr': 'FROM_BASE64( articles.article_title )', # строка порядок строк
                                    }
                                   )
    
            if len(getRez) == 0:
                raise err.WikiException( ARTICLE_NOT_FOUND )
            
            for oneObj in getRez:
    #             logging.info( 'list:: Before oneArt = ' + str(oneObj))
                
                oneObj.article_title = base64.b64decode(oneObj.title_text).decode(encoding='UTF-8')
                articleTitle = oneObj.article_title.strip().strip(" \t\n")
                oneObj.article_link =  articleTitle.lower().replace(' ','_')
#                 oneObj.article_html =  base64.b64decode(oneObj.article_html).decode(encoding='UTF-8')

#         logging.info( 'article:: revisionsList:::  str(len(getRez)) = ' + str(len(getRez)))
#         logging.info( 'article:: revisionsList:::  getRez = ' + str(getRez))
            return getRez

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


#########################################################################    
 
    def __init__ (self, id=0, title = ''): 
#         logging.info('article:: __init__')

        Model.__init__(self, 'articles')   
        self.article_id = id # эти параметры прилетают из формы редактирования
        self.article_title = title # эти параметры прилетают из формы редактирования
        self.article_annotation = '' # Это аннотация статьи!!!!!
        self.article_html = '' # эти параметры прилетают из формы редактирования
        self.category_article_id = config.options.info_page_categofy_id # категория страницы (служебные?) 'inf','trm','nvg','tpl'
        self.template = config.options.main_info_template
#         self.article_link = '' 

        

    def save(self, user_id, templateDir):
        """
        сохранить данные.
        2.1 если текст новый
        2.1.1 добавим новый запись в "article" и получим новую ИД
        2.1.2 добавим новую запись в "articles" с флагом "А" 
            хеш делаем из суммы текста и заголовка статьи 
        2.1.3 добавим новую запись в "titles" - хешируем название статьи, и хеш добавляем в таблицу.
        - 
        2.2 если текст поменялся
        2.2.1 поменяем запись в "article"
        2.2.2 в "articles" для текущего ИД  поменяем все флаги на "N"
        2.2.3 добавим новую запись в "articles" с флагом "А"
            хеш делаем из суммы заголовка статьи и текста,  и, 
            если в статье (название+РТФ) ничего не поменялось, то сохранить мы не сможем.
        2.2.4 добавим новую запись в "titles" - хешируем название статьи, и хеш добавляем в таблицу. 
            если название менялось, то запись будет добавлена  
        
        
        """

# categories 
# Это новая таблица  - все категории, которые только озможны, и пока там  
# вот такие категрии (служебные?) 'inf','trm','nvg','tpl'

#         artModel.article_id = self.get_argument("id", 0)
#         artModel.article_title = self.get_argument("article_title")
#         artModel.article_annotation = self.get_argument("article_annotation")
#         artModel.article_html = self.get_argument("article_html")

       
#         self.start_transaction()
# любая запись - это ревизия!
        revisionControl = self.RevisionLoc()
        titleControl = self.Title()
        annotationControl = self.Annotation()
        textControl = self.Text()       

        revisionControl.user_id = user_id

        titleControl.title_text = self.article_title.strip().strip(" \t\n")
#         del(self.article_title)
        titleText = titleControl.title_text.lower().replace(' ','_')
        titleControl.title_sha_hash = hashlib.sha256(
                                            tornado.escape.utf8(titleText)
                                            ).hexdigest()  #.decode(encoding='UTF-8')
        titleControl.title_text = base64.b64encode(tornado.escape.utf8(titleControl.title_text)).decode(encoding='UTF-8')

        annotationControl.annotation_sha_hash = hashlib.sha256(
                                               tornado.escape.utf8(self.article_annotation)
                                               ).hexdigest()   #.decode(encoding='UTF-8')
        annotationControl.annotation_text = base64.b64encode(tornado.escape.utf8(self.article_annotation)).decode(encoding='UTF-8')    
#         del(self.article_annotation)

#         wrkHtml = self.article_html
#         logging.info( 'wrkHtml = ' + repr(wrkHtml))
# вот ту, перед укладкой на хранение, надо будет очищать исходник от вставок... 
        textControl.text_html = base64.b64encode(
                                    zlib.compress(
                                        tornado.escape.utf8(self.article_html)
                                                )
                                                    ).decode(encoding='UTF-8')
        
        textControl.text_sha_hash = hashlib.sha256(
                                               tornado.escape.utf8(self.article_html)
                                               ).hexdigest()   #.decode(encoding='UTF-8')
                                               

#         logging.info( 'Article ::: save titleText  = ' + str(titleText))
#         logging.info( 'Article ::: save titleControl.title_text  = ' + str(titleControl.title_text))
#         logging.info( 'Article ::: save annotationControl.annotation_text  = ' + str(annotationControl.annotation_text))
 
        
# получили ХЭШИ с новых данных.                                            
# надо узнать,являются ли наши данные реально новыми        
        isUniqueRez = self.IsUniqueRevision(
                                            titleControl.title_sha_hash, 
                                            annotationControl.annotation_sha_hash, 
                                            textControl.text_sha_hash)

#         logging.info( 'SAVE::!!! isUniqueRez = ')
#         for oneRez in isUniqueRez:
#             logging.info( str(oneRez) )

        newText = True
        newAnnotation = True
        newTitle = True
        
        if len(isUniqueRez) > 0:
            for oneRez in isUniqueRez:
#                 logging.info( oneRez )
#                 if oneRez.article_id == self.article_id:
                if (oneRez.text_sha_hash == textControl.text_sha_hash):
                    newText = False
                if (oneRez.annotation_sha_hash == annotationControl.annotation_sha_hash):
                    newAnnotation = False
                if (oneRez.title_sha_hash == titleControl.title_sha_hash) :
                    newTitle = False

#             if not newText and not newAnnotation and not newTitle:
#                 raise err.WikiException(LINK_OR_ARTICLE_NOT_UNIQ)
                    
        logging.info( 'after Testing: self.article_id = ' + str(self.article_id) + '; newText = ' + str(newText) + '; newTitle = ' + str (newTitle) + '; newAnnotation = ' + str (newAnnotation) )

        revisionControl.title_sha_hash = titleControl.title_sha_hash
        revisionControl.annotation_sha_hash = annotationControl.annotation_sha_hash
        revisionControl.text_sha_hash = textControl.text_sha_hash

        
# вот тут нужна конверация!!!! и всякая иная обработка!!!!
#         htmlTextOut = wrkHtml
        # rtf2xml - то библиотека для переработки.
#         htmlTextOut = markdown.markdown(wrkHtml)
#  надо подготовить текст к публикации (возможно проанализаровать - есть ли в тексте какие - то данные, КОТОРЫЕ СТОИТ ОТДЛЬНО ОБРАБОТАТЬ.)
# Внешних шаблонов нагородить...         
        htmlTextOut = self.article_html
        self.article_html = base64.b64encode(tornado.escape.utf8(htmlTextOut)).decode(encoding='UTF-8') 
        self.article_title = titleControl.title_text
        self.article_annotation = annotationControl.annotation_text                                   
        
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
                        
                titleControl.article_id = self.article_id
                annotationControl.article_id = self.article_id
                textControl.article_id = self.article_id
            else:
                self.update('article_id = ' + str (self.article_id))
                
            if newText or newTitle or newAnnotation:
                revisionUpd = self.RevisionLoc()
                del(revisionUpd.revision_id) 
                del(revisionUpd.article_id) 
                del(revisionUpd.user_id) 
    #             del(revisionUpd.revision_date) 
                del(revisionUpd.title_sha_hash) 
                del(revisionUpd.annotation_sha_hash) 
                del(revisionUpd.text_sha_hash) 
    
                revisionUpd.revision_actual_flag = 'N'
                revisionUpd.update('article_id = ' + str (self.article_id))
                revisionControl.article_id =  self.article_id
                revisionControl.revision_actual_flag = 'A'
                revisionId = revisionControl.insert('revision_id')
                
                logging.info( 'after revisionControl.insert::: revisionId = ' + str(revisionId)  )
                logging.info( 'after revisionControl.insert::: self.article_id = ' + str(self.article_id) + '; newText = ' + str(newText) + '; newTitle = ' + str (newTitle) + '; newAnnotation = ' + str (newAnnotation) )
                
                if newText:
                    logging.info( 'SAVE!!!!!:: newText = ' + str(newText))
                    textControl.article_id = self.article_id
                    textControl.insert()
                     
                if newTitle:
                    titleControl.article_id = self.article_id
                    titleControl.insert()
                
                if newAnnotation:
                    annotationControl.article_id = self.article_id
                    annotationControl.insert()
    
                self.commit()
        
# вот после всего надо сохранить шаблон в шаблоновую директорию... 
                logging.info( 'save:: save self.category_article_id = ' + str(self.category_article_id))
                logging.info( 'save:: save 2 self.category_article_id = ' + str(int(self.category_article_id)))
                logging.info( 'save:: save config.options.tpl_categofy_id = ' + str(config.options.tpl_categofy_id))
                logging.info( 'save:: save 2 config.options.tpl_categofy_id = ' + str(int(config.options.tpl_categofy_id)))
                logging.info( 'save:: save self.article_id = ' + str(self.article_id))
                
                if int(self.category_article_id) == int(config.options.tpl_categofy_id):
                    logging.info( 'save:: save Template! = ' )
                     
                    wrkTpl = Template()
                    wrkTpl.save(self.article_id, htmlTextOut, templateDir)


        except Exception as e:
            logging.info( 'Save:: Exception as et = ' + str(e))
            self.rollback()
             
        self.article_link = titleText.lower().replace(' ','_') 
        logging.info( 'save:: save self.article_link! = ' + self.article_link )
                
        return self 
         



    def get(self, articleTitle):
         """
         получить статью по названию (одну) - функция для пердставления данных (!!!) 
         получить ОЛЬКО опубликованный текст  (активную статью) - для редактирования получаем статью иным образом! 
    
         - по одному из имен (старых - новых не важно) 
         выбираем данные из "article" и "articles" берем как ХТМЛ, так и РТФ ну и активный тайтл (ил "articles")
         имя ищем по ХЕШУ в таблице "titles"
         
         """
         logging.info( 'Article ::: get articleTitle  = ' + str(articleTitle))
    
         articleTitle = hashlib.sha256(
                                     tornado.escape.utf8(articleTitle)
                                     ).hexdigest()  #.decode(encoding='UTF-8')
    
    
         getRez = self.select(
                                'articles.article_id, revisions.revision_id, articles.article_title, ' + 
                                'articles.article_annotation,  articles.article_html, articles.category_article_id, articles.template ',
                                ' revisions, titles lfind ',
                                    {
                                'whereStr': " articles.article_id = lfind.article_id " +
                                             " AND revisions.revision_actual_flag = 'A' " +
                                             " AND revisions.article_id =  articles.article_id " +
                                             " AND articles.article_id = lfind.article_id " +
                                             " AND lfind.title_sha_hash = '" + articleTitle  + "' " , # строка набор условий для выбора строк
                                 }
                                )
    
         if len(getRez) == 0:
            raise err.WikiException( ARTICLE_NOT_FOUND )
         elif len(getRez) == 1:   
    #             logging.info( 'getRez = ' + str(getRez[0]))
             outArt = getRez[0]
             outArt.article_title = base64.b64decode(outArt.article_title).decode(encoding='UTF-8')
             outArt.article_annotation = base64.b64decode(outArt.article_annotation).decode(encoding='UTF-8')
             outArt.article_html =  base64.b64decode(outArt.article_html).decode(encoding='UTF-8')
    #             logging.info( 'outArt.article_html = ' + str(outArt.article_html))
    
             articleTitle = outArt.article_title.strip().strip(" \t\n")
             outArt.article_link =  articleTitle.lower().replace(' ','_')
             
             return outArt


    def getById(self, articleId):
         """
         получить статью по ID (одну) - функция для пердставления данных (!!!) 
         получить ОЛЬКО опубликованный текст  (активную статью) - для редактирования получаем статью иным образом! 
    
         """
         logging.info( 'Article ::: getById articleId  = ' + str(articleId))
    
         getRez = self.select(
                                'articles.article_id, revisions.revision_id, articles.article_title, '+
                                'articles.article_annotation,  articles.article_html, articles.category_article_id, articles.template',
                                ' revisions ',
                                    {
                                'whereStr': ' articles.article_id = ' + str(articleId) + 
                                             " AND revisions.revision_actual_flag = 'A' " +
                                             ' AND revisions.article_id =  articles.article_id ' ,
                                 }
                                )
    
         if len(getRez) == 0:
            raise err.WikiException( ARTICLE_NOT_FOUND )
         elif len(getRez) == 1:   
#              logging.info( ' getById getRez = ' + str(getRez[0]))
             outArt = getRez[0]
             outArt.article_title = base64.b64decode(outArt.article_title).decode(encoding='UTF-8')
             outArt.article_annotation = base64.b64decode(outArt.article_annotation).decode(encoding='UTF-8')
             outArt.article_html =  base64.b64decode(outArt.article_html).decode(encoding='UTF-8')
    #             logging.info( 'outArt.article_html = ' + str(outArt.article_html))
    
             articleTitle = outArt.article_title.strip().strip(" \t\n")
             outArt.article_link =  articleTitle.lower().replace(' ','_')
             
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
             categoryStr = ' AND articles.category_article_id = ' + str(categoryId)
             
         getRez = self.select(
    #                                'articles.article_id, FROM_BASE64(articles.article_title),  FROM_BASE64(articles.article_html) ',
                                'articles.article_id, revisions.revision_id, articles.article_title, ' +
                                'articles.article_annotation, articles.category_article_id, articles.template ',
                                ' revisions ',
                                    {
                                'whereStr': ' articles.article_id = revisions.article_id '  +
                                         " AND revisions.revision_actual_flag = 'A' " + categoryStr, # строка набор условий для выбора строк
                                'orderStr': ' articles.article_id ', # строка порядок строк
    #                                'orderStr': 'FROM_BASE64( articles.article_title )', # строка порядок строк
                                 }
                                )
    
         logging.info( 'list:: getRez = ' + str(getRez))
         if len(getRez) == 0:
#             raise err.WikiException( ARTICLE_NOT_FOUND )
            return []
         
         for oneObj in getRez:
             oneObj.article_title = base64.b64decode(oneObj.article_title).decode(encoding='UTF-8')
             articleTitle = oneObj.article_title.strip().strip(" \t\n")
             oneObj.article_link  =  articleTitle.lower().replace(' ','_')
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

        - выбираем данные из "revisions"  и "titles"  и "users" 
        """
        revControl = self.RevisionLoc()
        return revControl.revisionsList(articleId)


    def IsUniqueRevision(self, titleHash, annotationHash, articleHash):
        """
        проверить, является ли данная ревизия уникальной 
        - может поменятся все, 
        - пожет - заглавие
        - может текст
        """
        revControl = self.RevisionLoc()
        return revControl.IsUniqueRevision(titleHash, annotationHash, articleHash)



class Revision(Article):
        def __init__ (self): 
            Article.__init__(self)   










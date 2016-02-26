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
import pymysql

import hashlib
import base64
        

from _overlapped import NULL

##############
from . import Model
from . import err



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
    - любые смены в "article_title" - сразу записываются как новый хеш в таблицу "links"  
    поиск статьи по ее названию  (по любым старым названиям) делается по хешам в таблице  "links"
    - актуальный текст сразу готовится к изданию, и помещается в таблицу "published"
    
    статья Это:
    - заглавие
    - текст стаьи (актуальный)
    
    - категория статьи (category)
        информационная    inf
        термин            trm
        навигационная     nvg
        шабон             tpl
    - шабон статьи (template)
        ??? 
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
    2.1.3 добавим новую запись в "links" - хешируем название статьи, и хеш добавляем в таблицу.
    - 
    2.2 если текст поменялся
    2.2.1 поменяем запись в "published"
    2.2.2 в "articles" для текущего ИД  поменяем все флаги на "N"
    2.2.3 добавим новую запись в "articles" с флагом "А"
        хеш делаем из суммы заголовка статьи и текста,  и, 
        если в статье (название+РТФ) ничего не поменялось, то сохранить мы не сможем.
    2.2.4 добавим новую запись в "links" - хешируем название статьи, и хеш добавляем в таблицу. 
        если название менялось, то запись будет добавлена  
    2.3 в любом случае делается запись о новой ревизии "revisions". 
        (автор, хеш статьи, хеш заголовка, дата...)
    
    получить список статей 
    - выбираем данные из "published" - 
    
    получить одну статью 
    - по одному из имен (старых - новых не важно) 
    выбираем данные из "published" и "articles" берем как ХТМЛ, так и РТФ ну и активный тайтл (ил "articles")
    имя ищем по ХЕШУ в таблице "links"
    
    получить историю статьи 
    - по  ИД (одному из имен) выбрать все версии статьи из "revisions"
    
    """

#########################################################################    
 
    class Text(Model):
        def __init__ (self): 
            Model.__init__(self, 'texts')   
            self.article_id = 0
            self.article_html = '' 
            self.article_sha_hash = ''

        def get2Edit( self, articleId, revisionId ):
            """
            получить ОДНУ ревизию статьи        
            
            Это делаем для РЕДАКТИРОВНИЯ!!!
            
            """
    
            getRez = self.select(
                                   'texts.article_id, revisions.revision_id, texts.article_html,  links.article_title, ' +
                                   ' UNIX_TIMESTAMP(revisions.revision_date) AS revision_date, revisions.user_id, revisions.revision_actual_flag ' ,
                                   'links, revisions',
                                       {
                                   'whereStr': '  texts.article_sha_hash =  revisions.article_sha_hash' +
                                                ' AND links.link_sha_hash = revisions.link_sha_hash ' +
                                                ' AND revisions.revision_id = ' + revisionId  + ' ' +
                                                ' AND revisions.article_id = ' + articleId  + ' '   #### строка набор условий для выбора строк
                                    }
                                   )
    
            if len(getRez) == 0:
                raise err.WikiException( ARTICLE_NOT_FOUND )
            elif len(getRez) == 1:   
    #             logging.info( 'getRez = ' + str(getRez[0]))
                outArt = getRez[0]
                outArt.article_title = base64.b64decode(outArt.article_title).decode(encoding='UTF-8')
                decodeText =  base64.b64decode(outArt.article_html)
                outArt.article_html = zlib.decompress(decodeText).decode('UTF-8')    
    #             logging.info( 'outArt.article_html = ' + str(outArt.article_html))
    
                articleTitle = outArt.article_title.strip().strip(" \t\n")
                outArt.article_link =  articleTitle.lower().replace(' ','_')
                
                return outArt

   
    class Link(Model):
        def __init__ (self): 
            Model.__init__(self, 'links')   
            self.article_id = 0
            self.article_title = ''
            self.link_sha_hash = ''


    class RevisionLoc(Model):
        def __init__ (self): 
            Model.__init__(self, 'revisions')   
            self.revision_id = 0
            self.article_id = 0
            self.user_id = 0
# дата создания ревизии   
#             self.revision_date = 0
#             self.revision_actual_flag  = 'A'
            self.link_sha_hash = ''
            self.article_sha_hash = ''

        def revisionsList(self, articleId):
            """
            получить список ревизий для одной статей
            упорядочивать по дате ревизии - в начале - самые последние
            Обязательно - автора!
    
    
            - выбираем данные из "articles"  и "links"  и "users" 
            
            
            """
            getRez = self.select(
    #                                'articles.article_id, FROM_BASE64(articles.article_title),  FROM_BASE64(articles.article_html) ',
                                   ' UNIX_TIMESTAMP(revisions.revision_date) AS revision_date, '+ 
                                   ' revisions.article_id, revisions.revision_id, links.article_title, ' +
                                   ' users.user_id, users.user_name ',
                                   ' links, users ',
                                       {
                                   'whereStr': ' revisions.link_sha_hash = links.link_sha_hash '  +
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
                
                oneObj.article_title = base64.b64decode(oneObj.article_title).decode(encoding='UTF-8')
                articleTitle = oneObj.article_title.strip().strip(" \t\n")
                oneObj.article_link =  articleTitle.lower().replace(' ','_')
#                 oneObj.article_html =  base64.b64decode(oneObj.article_html).decode(encoding='UTF-8')

#         logging.info( 'article:: revisionsList:::  str(len(getRez)) = ' + str(len(getRez)))
#         logging.info( 'article:: revisionsList:::  getRez = ' + str(getRez))
            return getRez

        def IsUniqueRevision(self, linkHash, articleHash):
            """
            проверить, является ли данная ревизия уникальной 
            - может поменятся все, 
            - пожет - заглавие
            - может текст
            """
            isUniqueRez = self.select(
                       ' revisions.article_sha_hash, revLink.link_sha_hash',
                       'revisions revLink',
                           {
                       'whereStr': ' (revisions.article_sha_hash = "'+ articleHash + '" '
                                    ' OR revLink.link_sha_hash = "' + linkHash  + '") ' , # строка набор условий для выбора строк
                        }
                       )
            
            return isUniqueRez


#########################################################################    
 
    def __init__ (self): 
#         logging.info('article:: __init__')

        Model.__init__(self, 'articles')   
        self.article_id = 0 # эти параметры прилетают из формы редактирования
        self.article_title = '' # эти параметры прилетают из формы редактирования
        self.article_html = '' # эти параметры прилетают из формы редактирования

        

    def save(self, user_id):
        """
        сохранить данные.
        2.1 если текст новый
        2.1.1 добавим новый запись в "article" и получим новую ИД
        2.1.2 добавим новую запись в "articles" с флагом "А" 
            хеш делаем из суммы текста и заголовка статьи 
        2.1.3 добавим новую запись в "links" - хешируем название статьи, и хеш добавляем в таблицу.
        - 
        2.2 если текст поменялся
        2.2.1 поменяем запись в "article"
        2.2.2 в "articles" для текущего ИД  поменяем все флаги на "N"
        2.2.3 добавим новую запись в "articles" с флагом "А"
            хеш делаем из суммы заголовка статьи и текста,  и, 
            если в статье (название+РТФ) ничего не поменялось, то сохранить мы не сможем.
        2.2.4 добавим новую запись в "links" - хешируем название статьи, и хеш добавляем в таблицу. 
            если название менялось, то запись будет добавлена  
        
        
        """

       
#         self.start_transaction()
# любая запись - это ревизия!
        revision = self.RevisionLoc()
        linkControl = self.Link()
        textControl = self.Text()       

        revision.user_id = user_id

        wrkHtml = self.article_html
#         logging.info( 'wrkHtml = ' + repr(wrkHtml))
        textControl.article_html = base64.b64encode(zlib.compress(tornado.escape.utf8(self.article_html))).decode(encoding='UTF-8')
        textControl.article_sha_hash = hashlib.sha256(
                                               tornado.escape.utf8(self.article_html)
                                               ).hexdigest()   #.decode(encoding='UTF-8')
        linkControl.article_title = self.article_title.strip().strip(" \t\n")
        del(self.article_title)
        linkText = linkControl.article_title.lower().replace(' ','_')
        logging.info( 'Article ::: save linkControl.article_title  = ' + str(linkControl.article_title))
        logging.info( 'Article ::: save linkText  = ' + str(linkText))
        linkControl.link_sha_hash = hashlib.sha256(
                                            tornado.escape.utf8(linkText)
                                            ).hexdigest()  #.decode(encoding='UTF-8')
        linkControl.article_title = base64.b64encode(tornado.escape.utf8(linkControl.article_title)).decode(encoding='UTF-8')
 
        revision.link_sha_hash = linkControl.link_sha_hash
        revision.article_sha_hash = textControl.article_sha_hash
# получили ХЭШИ с новых данных.                                            
# надо узнать,являются ли наши данные реально новыми        
        isUniqueRez = self.IsUniqueRevision(linkControl.link_sha_hash, textControl.article_sha_hash)

#         logging.info( 'SAVE::!!! isUniqueRez = ')
#         for oneRez in isUniqueRez:
#             logging.info( str(oneRez) )

        newRtf = True
        newTitle = True
        
        if len(isUniqueRez) > 0:
            for oneRez in isUniqueRez:
#                 logging.info( oneRez )
#                 if oneRez.article_id == self.article_id:
                if (oneRez.article_sha_hash == textControl.article_sha_hash):
                    newRtf = False
                if (oneRez.link_sha_hash == linkControl.link_sha_hash) :
                    newTitle = False
            if not newRtf and not newTitle:
                raise err.WikiException(LINK_OR_ARTICLE_NOT_UNIQ)
                    
        logging.info( 'after Testing: self.article_id = ' + str(self.article_id) + '; newRtf = ' + str(newRtf) + '; newTitle = ' + str (newTitle) )

        
# вот тут нужна конверация!!!! и всякая иная обработка!!!!
#         htmlTextOut = wrkHtml
        # rtf2xml - то библиотека для переработки.
#         htmlTextOut = markdown.markdown(wrkHtml)
#  надо подготовить текст к публикации (возможно проанализаровать - есть ли в тексте какие - то данные, КОТОРЫЕ СТОИТ ОТДЛЬНО ОБРАБОТАТЬ.)        
        htmlTextOut = wrkHtml
        self.article_html = base64.b64encode(tornado.escape.utf8(htmlTextOut)).decode(encoding='UTF-8') 
        self.article_title =  linkControl.article_title
        
        if self.article_id == 0:
            if len(isUniqueRez) > 0:
                raise err.WikiException(LINK_OR_ARTICLE_NOT_UNIQ)
            
#             del(self.article_id)
            self.article_id = self.insert('article_id')
            linkControl.article_id = self.article_id
            textControl.article_id = self.article_id
#             self.commit()
            linkControl.insert() # запомним линку
#             self.commit()
            textControl.insert() # запомним статью
#             self.commit()

        else:
 
            revisionUpd = self.RevisionLoc()
            del(revisionUpd.revision_id) 
            del(revisionUpd.article_id) 
            del(revisionUpd.user_id) 
#             del(revisionUpd.revision_date) 
            del(revisionUpd.link_sha_hash) 
            del(revisionUpd.article_sha_hash) 
            revisionUpd.revision_actual_flag = 'N'
            revisionUpd.update('article_id = ' + str (self.article_id))
#             revisionUpd.commit()
           
            textControl.article_id = self.article_id
            if len(isUniqueRez) == 0 or newRtf:
                textControl.insert()
#                 self.commit()
                 
            linkControl.article_id = self.article_id
            if len(isUniqueRez) == 0 or newTitle:
                linkControl.insert()
 
#             else:
#                 raise err.WikiException(LINK_OR_ARTICLE_NOT_UNIQ)
            

#             del(self.article_id) 
            self.update('article_id = ' + str (self.article_id))
            self.commit()
             
#             published.article_id =  self.article_id
        self.article_link = linkText
# а вот ту надо добавить новую запись в таблицу ревизий!!
        revision.article_id =  self.article_id
        revision.insert()
                
        self.commit()
        return True 

    def get(self, articleLink):
         """
         получить статью по названию (одну) - функция для пердставления данных (!!!) 
         получить ОЛЬКО опубликованный текст  (активную статью) - для редактирования получаем статью иным образом! 
    
         - по одному из имен (старых - новых не важно) 
         выбираем данные из "article" и "articles" берем как ХТМЛ, так и РТФ ну и активный тайтл (ил "articles")
         имя ищем по ХЕШУ в таблице "links"
         
         """
         logging.info( 'Article ::: get articleLink  = ' + str(articleLink))
    
         articleTitle = hashlib.sha256(
                                     tornado.escape.utf8(articleLink)
                                     ).hexdigest()  #.decode(encoding='UTF-8')
    
    
         getRez = self.select(
                                'articles.article_id, revisions.revision_id, articles.article_title,  articles.article_html ',
                                ' revisions, links lfind ',
                                    {
                                'whereStr': ' articles.article_id = lfind.article_id ' +
                                             ' AND revisions.revision_actual_flag = "A" ' +
                                             ' AND revisions.article_id =  articles.article_id ' +
                                             ' AND articles.article_id = lfind.article_id ' +
                                             ' AND lfind.link_sha_hash = "' + articleTitle  + '" ' , # строка набор условий для выбора строк
                                 }
                                )
    
         if len(getRez) == 0:
             raise err.WikiException( ARTICLE_NOT_FOUND )
         elif len(getRez) == 1:   
    #             logging.info( 'getRez = ' + str(getRez[0]))
             outArt = getRez[0]
             outArt.article_title = base64.b64decode(outArt.article_title).decode(encoding='UTF-8')
             outArt.article_html =  base64.b64decode(outArt.article_html).decode(encoding='UTF-8')
    #             logging.info( 'outArt.article_html = ' + str(outArt.article_html))
    
             articleTitle = outArt.article_title.strip().strip(" \t\n")
             outArt.article_link =  articleTitle.lower().replace(' ','_')
             
             return outArt
    
    def list(self):
         """
         получить список статей
         упорядочивать потом будем
    
         получить список статей 
         - выбираем данные из "articles" - получить при этом АКТАЛЬНЫЕ ИД ревизий!
                 
         """
    
         getRez = self.select(
    #                                'articles.article_id, FROM_BASE64(articles.article_title),  FROM_BASE64(articles.article_html) ',
                                'articles.article_id, revisions.revision_id, articles.article_title,  articles.article_html ',
                                ' revisions ',
                                    {
                                'whereStr': ' articles.article_id = revisions.article_id '  +
                                         ' AND revisions.revision_actual_flag = "A" ', # строка набор условий для выбора строк
                                'orderStr': ' articles.article_id ', # строка порядок строк
    #                                'orderStr': 'FROM_BASE64( articles.article_title )', # строка порядок строк
                                 }
                                )
    
         if len(getRez) == 0:
             return None
    #                 raise err.WikiException( ARTICLE_NOT_FOUND )
         
         for oneObj in getRez:
    #             logging.info( 'list:: Before oneArt = ' + str(oneObj))
             
             oneObj.article_title = base64.b64decode(oneObj.article_title).decode(encoding='UTF-8')
             articleTitle = oneObj.article_title.strip().strip(" \t\n")
             oneObj.article_link =  articleTitle.lower().replace(' ','_')
             oneObj.article_html =  base64.b64decode(oneObj.article_html).decode(encoding='UTF-8')
    
    #             logging.info( 'list:: After oneArt = ' + str(oneObj))
    
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

        - выбираем данные из "revisions"  и "links"  и "users" 
        """
        revControl = self.RevisionLoc()
        return revControl.revisionsList(articleId)


    def IsUniqueRevision(self, linkHash, articleHash):
        """
        проверить, является ли данная ревизия уникальной 
        - может поменятся все, 
        - пожет - заглавие
        - может текст
        """
        revControl = self.RevisionLoc()
        return revControl.IsUniqueRevision(linkHash, articleHash)



class Revision(Article):
        def __init__ (self): 
            Article.__init__(self)   






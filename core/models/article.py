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
                                   'texts.article_id, revisions.revision_id, texts.text_html, subjects.subject_text, titles.title_text, ' +
                                   ' UNIX_TIMESTAMP(revisions.revision_date) AS revision_date, revisions.user_id, revisions.revision_actual_flag ' ,
                                   'titles, revisions, subjects',
                                       {
                                   'whereStr': '  texts.text_sha_hash =  revisions.text_sha_hash' +
                                                ' AND titles.title_sha_hash = revisions.title_sha_hash ' +
                                                ' AND subjects.subject_sha_hash = revisions.subject_sha_hash ' +
                                                ' AND revisions.revision_id = ' + revisionId  + ' ' +
                                                ' AND revisions.article_id = ' + articleId  + ' '   #### строка набор условий для выбора строк
                                    }
                                   )
    
            if len(getRez) == 0:
                raise err.WikiException( ARTICLE_NOT_FOUND )
            elif len(getRez) == 1:   
    #             logging.info( 'getRez = ' + str(getRez[0]))
                outArt = getRez[0]
                outArt.article_title = base64.b64decode(outArt.title_text).decode(encoding='UTF-8')
                outArt.article_subj = base64.b64decode(outArt.subject_text).decode(encoding='UTF-8')
                decodeText =  base64.b64decode(outArt.text_html)
                outArt.article_html = zlib.decompress(decodeText).decode('UTF-8')    
    #             logging.info( 'outArt.article_html = ' + str(outArt.article_html))
    
                articleTitle = outArt.article_title.strip().strip(" \t\n")
                outArt.article_link =  articleTitle.lower().replace(' ','_')
#                 self.article_link = titleText
                
                del(outArt.title_text) 
                del(outArt.text_html) 
                del(outArt.subject_text) 

                logging.info( 'TEXT ::: get2Edit outArt  = ' + str(outArt))
                 
                return outArt




    class Subj(Model):
        """
        Это возможность работать и менять 
        "кракое описание страницы" 
        Это поле будет использоваться при прсмотре списка статей.... 
        ну при показе - редактировании, так то само-собой.
        """
        def __init__ (self): 
            Model.__init__(self, 'subjects')   
            self.article_id = 0
            self.subject_text = ''
            self.subject_sha_hash = ''


   
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
            self.subject_sha_hash = ''
            self.text_sha_hash = ''

        def revisionsList(self, articleId):
            """
            получить список ревизий для одной статей
            упорядочивать по дате ревизии - в начале - самые последние
            Обязательно - автора!
    
    
            - выбираем данные из "texts"  и "subjects"  и "titles"  и "users" 
            
            
            """
            getRez = self.select(
    #                                'articles.article_id, FROM_BASE64(articles.article_title),  FROM_BASE64(articles.article_html) ',
                                   ' UNIX_TIMESTAMP(revisions.revision_date) AS revision_date, '+ 
                                   ' revisions.article_id, revisions.revision_id, ' +
                                   ' titles.title_text, subjects.subject_text, ' +
                                   ' users.user_id, users.user_name ',
                                   ' titles, subjects, users ',
                                       {
                                   'whereStr': ' revisions.title_sha_hash = titles.title_sha_hash '  +
                                            ' AND revisions.subject_sha_hash = subjects.subject_sha_hash '  +
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

        def IsUniqueRevision(self, titleHash, subjHash, textHash):
            """
            проверить, является ли данная ревизия уникальной 
            - может поменятся все, 
            - может - заглавие
            - может - аннотация
            - может текст
            """
            isUniqueRez = self.select(
                       ' revisions.text_sha_hash, revSubj.subject_sha_hash, revTitle.title_sha_hash',
                       'revisions revTitle, revisions revSubj',
                           { 
                       'whereStr': ' ( revTitle.title_sha_hash = "'+ titleHash + '" ' +
                                    ' OR revSubj.subject_sha_hash = "'+ subjHash + '" ' +
                                    ' OR revisions.text_sha_hash = "' + textHash  + '" ) ' , # строка набор условий для выбора строк
                        }
                       )
            
            return isUniqueRez


#########################################################################    
 
    def __init__ (self): 
#         logging.info('article:: __init__')

        Model.__init__(self, 'articles')   
        self.article_id = 0 # эти параметры прилетают из формы редактирования
        self.article_title = '' # эти параметры прилетают из формы редактирования
        self.article_subj = '' # Это аннотация статьи!!!!!
        self.article_html = '' # эти параметры прилетают из формы редактирования
        self.category_article_id = 0 # категория страницы (служебные?) 'inf','trm','nvg','tpl'
#         self.article_link = '' 

        

    def save(self, user_id):
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
#         artModel.article_subj = self.get_argument("article_subj")
#         artModel.article_html = self.get_argument("article_html")

       
#         self.start_transaction()
# любая запись - это ревизия!
        revisionControl = self.RevisionLoc()
        titleControl = self.Title()
        subjControl = self.Subj()
        textControl = self.Text()       

        revisionControl.user_id = user_id

        titleControl.title_text = self.article_title.strip().strip(" \t\n")
#         del(self.article_title)
        titleText = titleControl.title_text.lower().replace(' ','_')
        titleControl.title_sha_hash = hashlib.sha256(
                                            tornado.escape.utf8(titleText)
                                            ).hexdigest()  #.decode(encoding='UTF-8')
        titleControl.title_text = base64.b64encode(tornado.escape.utf8(titleControl.title_text)).decode(encoding='UTF-8')

        subjControl.subject_sha_hash = hashlib.sha256(
                                               tornado.escape.utf8(self.article_subj)
                                               ).hexdigest()   #.decode(encoding='UTF-8')
        subjControl.subject_text = base64.b64encode(tornado.escape.utf8(self.article_subj)).decode(encoding='UTF-8')    
#         del(self.article_subj)

        wrkHtml = self.article_html
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
#         logging.info( 'Article ::: save subjControl.subject_text  = ' + str(subjControl.subject_text))
 
        
# получили ХЭШИ с новых данных.                                            
# надо узнать,являются ли наши данные реально новыми        
        isUniqueRez = self.IsUniqueRevision(
                                            titleControl.title_sha_hash, 
                                            subjControl.subject_sha_hash, 
                                            textControl.text_sha_hash)

#         logging.info( 'SAVE::!!! isUniqueRez = ')
#         for oneRez in isUniqueRez:
#             logging.info( str(oneRez) )

        newText = True
        newSubj = True
        newTitle = True
        
        if len(isUniqueRez) > 0:
            for oneRez in isUniqueRez:
#                 logging.info( oneRez )
#                 if oneRez.article_id == self.article_id:
                if (oneRez.text_sha_hash == textControl.text_sha_hash):
                    newText = False
                if (oneRez.subject_sha_hash == subjControl.subject_sha_hash):
                    newSubj = False
                if (oneRez.title_sha_hash == titleControl.title_sha_hash) :
                    newTitle = False

            logging.info( 'after Testing:newText = ' + str(newText) + '; newSubj = ' + str(newSubj) + '; newTitle = ' + str (newTitle) )

#             if not newText and not newSubj and not newTitle:
#                 raise err.WikiException(LINK_OR_ARTICLE_NOT_UNIQ)
                    
        logging.info( 'after Testing: self.article_id = ' + str(self.article_id) + '; newText = ' + str(newText) + '; newTitle = ' + str (newTitle) )

        revisionControl.title_sha_hash = titleControl.title_sha_hash
        revisionControl.subject_sha_hash = subjControl.subject_sha_hash
        revisionControl.text_sha_hash = textControl.text_sha_hash

        
# вот тут нужна конверация!!!! и всякая иная обработка!!!!
#         htmlTextOut = wrkHtml
        # rtf2xml - то библиотека для переработки.
#         htmlTextOut = markdown.markdown(wrkHtml)
#  надо подготовить текст к публикации (возможно проанализаровать - есть ли в тексте какие - то данные, КОТОРЫЕ СТОИТ ОТДЛЬНО ОБРАБОТАТЬ.)
# Внешних шаблонов нагородить...         
        htmlTextOut = wrkHtml
        self.article_html = base64.b64encode(tornado.escape.utf8(htmlTextOut)).decode(encoding='UTF-8') 
        self.article_title = titleControl.title_text
        self.article_subj = subjControl.subject_text                                   
        
        
        if self.article_id == 0:
            try:
                self.article_id = self.insert('article_id')
            except Exception as e:
# // pymysql.err.IntegrityError: (1062, "Duplicate entry '9153907302f2a10a1ffd58094528ab3361d3736654e3136cf26c7cbf828224a2' for key 'PRIMARY'")
                logging.info( 'ComposeHandler:: Exception as et = ' + str(e))
                return False
#                 raise e
#             err.WikiException(LINK_OR_ARTICLE_NOT_UNIQ)

            self.commit
                    
            titleControl.article_id = self.article_id
            subjControl.article_id = self.article_id
            textControl.article_id = self.article_id
        else:
            self.update('article_id = ' + str (self.article_id))
            self.commit()
            

        if newText or newTitle or newSubj:
            revisionUpd = self.RevisionLoc()
            del(revisionUpd.revision_id) 
            del(revisionUpd.article_id) 
            del(revisionUpd.user_id) 
#             del(revisionUpd.revision_date) 
            del(revisionUpd.title_sha_hash) 
            del(revisionUpd.subject_sha_hash) 
            del(revisionUpd.text_sha_hash) 

            revisionUpd.revision_actual_flag = 'N'
            revisionUpd.update('article_id = ' + str (self.article_id))
            revisionControl.article_id =  self.article_id
            revisionControl.insert()
            self.commit
            
        if newText:
            textControl.article_id = self.article_id
            textControl.insert()
            self.commit
             
        if newTitle:
            titleControl.article_id = self.article_id
            titleControl.insert()
            self.commit
        
        if newSubj:
            subjControl.article_id = self.article_id
            subjControl.insert()
            self.commit
             
#             published.article_id =  self.article_id
# а вот ту надо добавить новую запись в таблицу ревизий!!
        
        self.article_link = titleText
                
        return True 

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
                                'articles.article_id, revisions.revision_id, articles.article_title,  articles.article_subj,  articles.article_html ',
                                ' revisions, titles lfind ',
                                    {
                                'whereStr': ' articles.article_id = lfind.article_id ' +
                                             ' AND revisions.revision_actual_flag = "A" ' +
                                             ' AND revisions.article_id =  articles.article_id ' +
                                             ' AND articles.article_id = lfind.article_id ' +
                                             ' AND lfind.title_sha_hash = "' + articleTitle  + '" ' , # строка набор условий для выбора строк
                                 }
                                )
    
         if len(getRez) == 0:
             raise err.WikiException( ARTICLE_NOT_FOUND )
         elif len(getRez) == 1:   
    #             logging.info( 'getRez = ' + str(getRez[0]))
             outArt = getRez[0]
             outArt.article_title = base64.b64decode(outArt.article_title).decode(encoding='UTF-8')
             outArt.article_subj = base64.b64decode(outArt.article_subj).decode(encoding='UTF-8')
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
                                'articles.article_id, revisions.revision_id, articles.article_title,  articles.article_subj ',
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
#              oneObj.article_title =  articleTitle.lower().replace(' ','_')
             oneObj.article_link  =  articleTitle.lower().replace(' ','_')
             oneObj.article_subj =  base64.b64decode(oneObj.article_subj).decode(encoding='UTF-8')
    
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

        - выбираем данные из "revisions"  и "titles"  и "users" 
        """
        revControl = self.RevisionLoc()
        return revControl.revisionsList(articleId)


    def IsUniqueRevision(self, titleHash, subjHash, articleHash):
        """
        проверить, является ли данная ревизия уникальной 
        - может поменятся все, 
        - пожет - заглавие
        - может текст
        """
        revControl = self.RevisionLoc()
        return revControl.IsUniqueRevision(titleHash, subjHash, articleHash)



class Revision(Article):
        def __init__ (self): 
            Article.__init__(self)   






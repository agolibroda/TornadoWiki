#!/usr/bin/env python
#
# Copyright 2016 Alec Goliboda
#
# article.py
# контроллер для загрузки и сохранению статей...



import logging
import json

import bcrypt
import concurrent.futures

import os.path
import re
import subprocess


import config

import core.models

from core.models.author     import Author
from core.models.article    import Article
from core.models.file       import File
from core.models.group      import Group

from core.WikiException     import *


class HelperArticle():
    """
    загрузить и сохранить статью
    
    """
    
    def __init__(self):
        self.artModel = Article()
        
    def setArticleTitle(self, articleName):
        self.artModel.article_title = articleName
        
    def setArticleCategiry(self, articleCategoryId):
        self.artModel.category_article_id = articleCategoryId
        
    def getModel(self):
        return self.artModel
    
    def setModel(self, article):
        self.artModel = article

    def getArticleById(self, articleId):
        logging.info( ' getArticleById:: articleId = ' + str(articleId))
        article = self.artModel.getById( articleId )
        if not article: raise tornado.web.HTTPError(404)
        fileModel = File()
# вот тут надо посмотреть - что - то не работает выбор файлов!!!!!!!
        fileList = fileModel.getFilesListForArticle( articleId, config.options.to_out_path)
            
#             logging.info( 'getArticleById:: article = ' + str(article))
#             logging.info( 'getArticleById:: fileList = ' + str(fileList))
        return (article, fileList)
     
     
    
    def getListArticles(self, categoryId = 0):
    
        try:
            rezult = self.artModel.list (categoryId)
            if not rezult: rezult = []
            logging.info( 'getListArticles:: rezult = ' + str(rezult))
            return  rezult #.result()
        except Exception as e:
            logging.info( 'getListArticles:: Exception as et = ' + str(e))
            error = Error ('500', 'что - то пошло не так :-( ')
            return []


    def getListArticlesByAutorId(self, authorId = 0, spectatorId = 0):
        """
        получить список статей одного автора
        
        """
        rezult = self.artModel.listByAutorId (authorId, spectatorId)
        if not rezult: rezult = []
#         logging.info( 'getListArticles:: rezult = ' + str(rezult))
        return  rezult #.result()



    def getArticleByIdRevId(self, articleId, revId):
        """
        получить определенную ревизию статьи
        
        """
 
        if articleId and revId:
            fileModel = File()
            article =  self.artModel.get2Edit(articleId, revId)
           
            fileList = fileModel.getFilesListForArticle( articleId, config.options.to_out_path)
            return (article, fileList)
            

        
    def getArticleByName(self, articleName, spectatorId):
        """
        получить статью по ее названию (не линка, а название!!!!! )
        хотя, по - идее, надо поредакитровать и сначала превратить навание в линку...
        
        articleName - базе64 - кодированное имя статьи
        spectatorId - ИД пользователя, которые ищет/смотрит статью!!!!!
        
        """
        fileModel = File()
        articleLink = articleName.strip().strip(" \t\n")
        article = self.artModel.get( articleLink, spectatorId )
        fileList =  fileModel.getFilesListForArticle( article.article_id, 
                                                    config.options.to_out_path)
        return (article, fileList)


    def getArticleHash(self, articleHash):
        """
        получить статью по ее ХЕШУ (не линка, а название!!!!! )
        хотя, по - идее, надо поредакитровать и сначала превратить навание в линку...
        
        """
        fileModel = File()
        article = self.artModel.getByUsingHash( articleHash )
        logging.info( ' getArticleHash:: article.article_id = ' + str(article.article_id))
        fileList =  fileModel.getFilesListForArticle( article.article_id, 
                                                    config.options.to_out_path)
        return (article, fileList)


    def сomposeArticleSave(self, author_id, templateDir, article_pgroipId):
        """
        сохранить статью
        
        """
        try:
            logging.info( 'сomposeArticleSave:: self.artModel = ' + str(self.artModel))
            article = self.artModel.save(author_id, templateDir)
            logging.info( 'сomposeArticleSave:: After Save^ article = ' + str(article))
            
            if int(article_pgroipId) > 0 :
                groupModel = Group()
#                 logging.info( 'сomposeArticleSave:: author_id = ' + str(author_id))
#                 logging.info( 'сomposeArticleSave:: article_pgroipId = ' + str(article_pgroipId))
#                 logging.info( 'сomposeArticleSave:: article.article_id = ' + str(article.article_id))
                groupModel.librarySave(int(author_id), int(article_pgroipId), int(article.article_id), 'W')
            return True
        except WikiException as e:   
#             WikiException( ARTICLE_NOT_FOUND )
            logging.info( 'сomposeArticleSave:: e = ' + str(e))
            return False

        


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

from core.models.author import Author
from core.models.article import Article
from core.models.file import File

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
        try:
            article = self.artModel.getById( articleId )
            if not article: raise tornado.web.HTTPError(404)
            fileModel = File()
# вот тут надо посмотреть - что - то не работает выбор файлов!!!!!!!
            fileList = fileModel.getFilesListForArticle( articleId, config.options.to_out_path)
                
#             logging.info( 'getArticleById:: article = ' + str(article))
#             logging.info( 'getArticleById:: fileList = ' + str(fileList))
            return (article, fileList)
        except WikiException as e:   
#             WikiException( ARTICLE_NOT_FOUND )
            logging.info( 'getArticleById::Have ERROR!!!  ' + str(e))
            if not article: raise tornado.web.HTTPError(404)
            else: return (article, [])
     
    
    def getListArticles(self, categoryId = 0):
    
        rezult = self.artModel.list (categoryId)
        if not rezult: rezult = []
        logging.info( 'getListArticles:: rezult = ' + str(rezult))
        return  rezult #.result()


    def getListArticlesByAutorId(self, authorId = 0):
        """
        получить список статей одного автора
        
        """
    
        rezult = self.artModel.listByAutorId (authorId)
        if not rezult: rezult = []
#         logging.info( 'getListArticles:: rezult = ' + str(rezult))
        return  rezult #.result()

    def getArticleByIdRevId(self, articleId, revId):
        """
        получить определенную ревизию статьи
        
        """
 
        if articleId and revId:
            fileModel = File()
            try:
                article =  self.artModel.get2Edit(articleId, revId)
               
                fileList = fileModel.getFilesListForArticle( articleId, config.options.to_out_path)
                return (article, fileList)
#             except Exception as e:   
            except WikiException as e:   
#             WikiException( ARTICLE_NOT_FOUND )
                logging.info( 'getArticleByIdRevId:: e = ' + str(e))
                return (self.artModel, [])


        
    def getArticleByName(self, articleName):
        """
        получить статью по ее названию (не линка, а название!!!!! )
        хотя, по - идее, надо поредакитровать и сначала превратить навание в линку...
        
        """
        fileModel = File()
        try:
            articleLink = articleName.strip().strip(" \t\n")
            article = self.artModel.get( articleLink )
            fileList =  fileModel.getFilesListForArticle( article.article_id, 
                                                        config.options.to_out_path)
            return (article, fileList)
        except WikiException as e:   
#             WikiException( ARTICLE_NOT_FOUND )
            logging.info( 'getArticleByName:: e = ' + str(e))
            return (self.artModel, [])


    def getArticleHash(self, articleHash):
        """
        получить статью по ее ХЕШУ (не линка, а название!!!!! )
        хотя, по - идее, надо поредакитровать и сначала превратить навание в линку...
        
        """
        fileModel = File()
        try:
            article = self.artModel.getByUsingHash( articleHash )
            logging.info( ' getArticleHash:: article.article_id = ' + str(article.article_id))
            fileList =  fileModel.getFilesListForArticle( article.article_id, 
                                                        config.options.to_out_path)
            return (article, fileList)
        except WikiException as e:   
#             WikiException( ARTICLE_NOT_FOUND )
            logging.info( 'getArticleByName:: e = ' + str(e))
            return (self.artModel, [])


    def сomposeArticle(self):
        """
        сохранить статью
        
        """
 

        


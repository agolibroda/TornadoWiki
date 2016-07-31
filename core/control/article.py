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

from core.models.user import User
from core.models.article import Article
from core.models.article import Revision
from core.models.file import File



class ControlArticle():
    """
    загрузить и сохранить статью
    """
    
    def getArticleById(self, articleId):
        logging.info( ' getArticleById:: articleId = ' + str(articleId))
        artModel = Article()
        article = artModel.getById( articleId )
        if not article: raise tornado.web.HTTPError(404)
        fileControl = File()
        fileList = fileControl.getFilesListForArticle(
                                          articleId, 
                                          config.options.to_out_path)
            
        logging.info( 'ArticleHandler:: fileList = ' + str(fileList))
        
    #     тут надо посмтреть что возвращать - массив или список, ну, и что потом получать...  
        
        return (article, fileList)
     
    
    def getListArticles(self):
    
        artModel = Article()
        rezult = artModel.list ()
        if not rezult: rezult = []
        logging.info( 'AdminFeedHandler:: rezult = ' + str(rezult))
        return  rezult #.result()


    def getArticleByIdRevId(self, articleId, revId):
        """
        получить определенную ревизию статьи
        
        """
 
        if articleId and revId:
            artModel = Article()
            article = yield executor.submit( artModel.get2Edit, articleId, revId)
           
            fileControl = File()
            fileList = yield executor.submit( 
                                          fileControl.getFilesListForArticle, 
                                          articleId, 
                                          config.options.to_out_path)
            return (article, fileList)

        
    def getArticleByName(self, articleName):
        """
        получить статью по ее названию (не линка, а название!!!!! )
        хотя, по - идее, надо поредакитровать и сначала превратить навание в линку...
        
        """
        articleLink = articleName.strip().strip(" \t\n")
        artModel = Article()
        article = artModel.get( articleLink )
        fileControl = File()
        logging.info( 'ArticleHandler:: article.article_id = ' + str(article.article_id))
        fileList = yield executor.submit( 
                                          fileControl.getFilesListForArticle, 
                                          article.article_id, 
                                          config.options.to_out_path)
        return (article, fileList)


    def сomposeArticle(self):
        """
        сохранить статью
        
        """
 

        


#!/usr/bin/env python
#
# Copyright 2016 Alec Goliboda
#
# file.py

from __future__ import print_function


import logging
import json

# import zlib
# import markdown

import tornado.options

import pymysql

import hashlib
import base64

import os.path
        

from _overlapped import NULL

##############
import config
from . import Model
from . import err
from .article import Article




class File(Model):
    """
    файл - это похоже, нечто из "терминов" 
    нпри клике на файл переходим на страницу описания теримна (файла) 
    если тип термина "файл", то даем большую картинку, и описание 
    и список страниц, в которых есть упоминание файла... 
    
    в общем, "термины"...
    типа:
    "строка" 
    "число"
    "файл"
    
    """

# Да, файлы переделать!!!!!
# - при загрузке файла сразу создается его статья, 
# линка на файл - сразу в ту статью помещаетмя,
# статью делаем в кроссе, с пометкой "М"
# ну и так далее...
# 
# птиродрахтель 
# только тем, кто любит труд вазелину принесут.

    class Kross(Model):
        """
        таблица перекрестных ссылок между 
        статьями и файлами. 
        файл может иметь много статй, статьи могут иметь много файлов. 
        """
        def __init__ (self): 
            Model.__init__(self, 'files_kroses')   
            self.file_id = 0
            self.article_id = 0
            self.file_kros_flag  = 'A' # Average : Main

        def save(self, file_id, article_id):
            self.file_id = file_id
            self.article_id = article_id
            self.insert()
                    
    
    def __init__(self):
        Model.__init__(self, 'files')   
        self.file_id = 0
        self.file_name = ''
        self.file_inside_name = ''
        self.file_extension = ''
        self.error = ''



    def getRealFileName(self, fname, storageDir):
        fNameList = list(fname)
        filePath = [fNameList[0]+fNameList[1], 
                    fNameList[2]+fNameList[3], 
                    fNameList[4]+fNameList[5], 
                    fNameList[6]+fNameList[7]]
#         logging.info( 'uploadOneFile filePath =  '+ str(filePath) )
        self.wrkDir = os.path.join(storageDir, '/'.join(filePath))
        return os.path.join(self.wrkDir, str(fname) + self.file_extension)
 
    def uploadOneFile(self, file, article_id, user_id):
        """
        загрузим файл, сделаем для него запись в табличке "файлы" 
        сделаем для него статью типа "термин" при попдании на страницу будет открываться файл и можно будет делать описание... 
        да, название статьи - === имени файла (из загрузки) 
        кстати, если вдруг такое название уже есть, то надо будет добавить нечо уникальное (дату)
        2 записи в кроссе - с флагом "Main" и "Average"
        """  
#         logging.info( 'uploadOneFile files = '  + str(files))
        
#         logging.info( 'uploadOneFile::  file = '  + str(file))
        self.file_name = file['filename']
#         logging.info( 'uploadOneFile:: post self.file_name =  '+ str(self.file_name) )
        self.file_extension = os.path.splitext(self.file_name)[1]
        fname = hashlib.sha256(file['body']).hexdigest()  
        self.realFileName = self.getRealFileName(fname, config.options.uploud_path)
#         logging.info( 'uploadOneFile realFileName =  ' + str(self.realFileName))
        try:
            if not os.path.exists(self.realFileName):
#  все здорово, файла нету, и его можно и загрузить и сохранить его имя в базу
                os.makedirs(self.wrkDir)
#                 logging.info( 'uploadOneFile LIKE CREATE! self.realFileName =  ' + str(self.realFileName))
                output_file = open( self.realFileName, 'wb')
                output_file.write(file['body'])
# вот теперь сохраним в базу.            
                self.save(fname, self.file_name, self.file_extension,  article_id, user_id)            
            else:
# если файл есть, то его надо найти в базе, по - имени, и отдать на выход ИД файла. 
                existingfile = self.loadFileNamedAndArticle(fname, article_id) 
#                 logging.info( 'file ::: save :: existingfile = ' + str(existingfile))
                if existingfile.article_id == None:
                    kross = self.Kross()
                    kross.save(existingfile.file_id, article_id)
                    
                self.file_id = existingfile.file_id 
                
#                 raise err.WikiException('File exist!')
        except  Exception as err:
            logging.error (' fale upload Error:: ' + str (err) )
            self.error = err
            
            
        return self    

#     @gen.coroutine
#     def post(self):
#         userloginLoad =  User()
# 
#         rezult = yield executor.submit( userloginLoad.login, self.get_argument("login"), self.get_argument("password") )
                        
   
    def upload(self, files, article_id, user_id):
        """
        Обработка очереди входных файлов 
        
        """  
#         logging.info( 'upload files = '  + str(files))
        
        rezult = []
        for oneFile in files['filearg']:
            fileOut = self.uploadOneFile(oneFile, article_id, user_id)
            rezult.append(fileOut)
        
        return rezult
                        
    def save(self, file_inside_name, fileName, fileExtension, article_id, user_id):
        """
        Запомнить описание файла. 
        имеем дело всегда с новыми файлами... 
        о, а что делать, если я решил поменять имя файлу?? 
        или, менять имя только у "майновой" страницы описания файла??
        
        """
        realFileName = self.realFileName
        del(self.realFileName)
        del(self.wrkDir)
        del(self.error)
        self.user_id = user_id
        self.file_name = fileName
        self.file_inside_name = file_inside_name
        self.file_extension = fileExtension
        self.insert('file_id')

        kross = self.Kross()
#         kross.file_kros_flag
        kross.save(self.file_id, article_id)
#       а вот теперь можно добавить и страницу с описанием самой картинки... 
#       а потом добавить туда и новый кросс... 

        artModel = Article()
        
        artModel.article_title =  self.file_name
        artModel.article_html =  self.file_name
        artModel.save ( user_id )
        
        kross.file_kros_flag = 'M'
        kross.save(self.file_id, artModel.article_id)

        
        self.realFileName = realFileName
        
        
    def loadFileNamed(self, file_inside_name):
        """
        загрузить полное описание файла, зная его внутренее (уникально) имя

        """
        getRez = self.select(
                               'files.file_id, files.file_inside_name, files.file_extension, files.file_name ',
                                '', #'links, published',
                                {
                               'whereStr': '  files.file_inside_name = "' + file_inside_name  + '" ' , # строка набор условий для выбора строк
                                }
                               )

        if len(getRez) == 0:
            raise err.WikiException( FILE_NOT_FOUND )
        else:   
            outFile = getRez[0]
            logging.info( 'file ::: loadFileNamed :: outFile = ' + str(outFile))
            
            outFile.realFileName = outFile.getRealFileName(outFile.file_inside_name)
            
            return outFile



    def loadFileNamedAndArticle(self, file_inside_name, article_id):
        getRez = self.select(
                               'files.file_id, files.file_inside_name, files.file_extension, files.file_name, fk.article_id AS article_id',
                                '',
                                   { 
                               'joinStr': ' LEFT JOIN files_kroses fk ON fk.file_id = files.file_id AND fk.article_id = ' + str(article_id) ,
                               'whereStr': ' files.file_inside_name = "' + file_inside_name  + '" ' , # строка набор условий для выбора строк
                                }
                               )

        if len(getRez) == 0:
            return None
#             raise err.WikiException( FILE_NOT_FOUND )
        else:   
            logging.info( 'file ::: loadFileNamed :: getRez = ' + str(getRez))
            outFile = getRez[0]
            logging.info( 'file ::: loadFileNamed :: outFile = ' + str(outFile))
            outFile.realFileName = outFile.getRealFileName(outFile.file_inside_name)
#             logging.info( 'file ::: loadFileNamed :: outFile = ' + str(outFile))
            
            return outFile
   
    def getFilesListForArticle(self, article_id, storageDir):
        getRez = self.select(
                               'files.file_id, files.file_inside_name, files.file_extension, files.file_name ',
                                '',
                                   { 
                               'joinStr': ' INNER JOIN files_kroses fk ON fk.file_id = files.file_id AND fk.article_id = ' + str(article_id) ,
#                                'whereStr': ' files.file_inside_name = "' + file_inside_name  + '" ' , # строка набор условий для выбора строк
                                }
                               )

        if len(getRez) == 0:
            return []
#             raise err.WikiException( FILE_NOT_FOUND )
        else:   
#             logging.info( 'file ::: loadFileNamed :: getRez = ' + str(getRez))
            outFile = getRez[0]
            for oneFile in getRez:
                oneFile.realFileName = oneFile.getRealFileName(oneFile.file_inside_name, storageDir)
                logging.info( 'file ::: loadFileNamed :: oneFile = ' + str(oneFile))
            return getRez

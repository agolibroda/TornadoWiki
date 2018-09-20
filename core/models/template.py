#!/usr/bin/env python
#
# Copyright 2015 Alec Goliboda
#
# template.py

# Это чисто работа с шаблонами 
# - выгрузить шаблон в шаблоновую директорию
# - удалить шаблон из директории



from __future__ import print_function


import logging

import tornado.options
import tornado.web


import os.path
        
# from _overlapped import NULL

##############
import config
from . import Model
from .. import WikiException 
# from . import Article

class Template(Model): #, tornado.web.RequestHandler):
    """
    Работа с шаблонами
    похоже, нужна процедура выкладки шаблона в особую директорию (ну, что бы не смешивать :-) )
    и выкладку делать будем в момент сохранения шаблона в форме :-) 
    
    self.get_template_path() - Это обращение к крассу "BaseHandler(tornado.web.RequestHandler):" 
    и где - то там, значит, надо назначать объект - "пользовательские шаблоны"  
    и вот тут его грузить :-) или, не грузить, а тут наследоватья от него....   
    
    
    """

    def __init__(self):
        self.file_name = ''
        self.file_extension = ''
        self.error = ''
        self.tmplateTxt = ''

    
    def load(self, template_id):
        """
        Польжить в директорию "внутренних" шаблонов файл шаблона,
        получив его тело из базы по ИД (если файла там нет) 
        
        """
        pass
    
    
    
    def clean(self, template_id, templateDir):
        """
        Убрать файл шаблона (по его ИД) из директории,
        в которой лежат все "внутрисистемные" шиблоны
        """
        pass


    def save(self, template_id, tmplateTxt, templateDir):
        """
        сохранить темплейт в директории... 
        
        
        """
        file_name = str(template_id)
        temptateDir = os.path.join(templateDir, config.options.tmpTplPath)
        temptateFileName = os.path.join(temptateDir, str(file_name) + config.options.tplExtension)
#         logging.info( 'Template:: save 3 temptateFileName =  ' + str(temptateFileName))

        output_file = open( temptateFileName, 'wb')
        output_file.write(bytes(tmplateTxt, 'utf-8'))
        output_file.close()


  


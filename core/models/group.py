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

import tornado.options
# import pymysql

import hashlib
import base64
        
from _overlapped import NULL

##############
import config


from . import Model
from .. import WikiException 

from core.models.template   import Template

from ..constants.data_base import * 


class Gpoup(Model):
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
    """
    
    def __init__(self, group_title = '', group_annotation = '', group_status = 'pbl'):
        self.group_id = 0
        self.group_title = group_title
        self.group_annotation = group_annotation
        self.group_status = group_status
        

    def get(self, group_id):
        pass
        
    def list(self, ):
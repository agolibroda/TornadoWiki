#!/usr/bin/env python
#
# Copyright 2015 Alec Goliboda
#
# err.py




from .constants.data_base import *


class WikiException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class Error():
    """
    просто класс для описания ошибок - 
    ч бы было удобнее их отдавать получателю.
    
    """
    def __init__(self, code, message):
        self.code = code
        self.message = message


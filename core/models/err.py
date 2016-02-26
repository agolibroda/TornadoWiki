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



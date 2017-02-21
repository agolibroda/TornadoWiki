#!/usr/bin/env python
#
# Copyright 2017 Alec Golibroda
#
# from core.Helpers      import *
# from core.Helpers      import TemplateParams
#


import logging


# from core.models.group      import Group



def splitAttributes(objOne):
    """
    разделить собственные параметры (без параметров с подчеркиваниями ) на 2 списка - 
    1 - список имен параметров
    2 - значений параметров 
    это нужно для того, что бы использовать все параметры в операции 
    добавления или изменения данных в базе данных.
    
    На выходе получим словарь из двух списков  
    """ 
#         objDict = objOne.__dict__
    objValuesNameList = list(objOne.__dict__.keys())
    listAttrNames = []
    listAttrValues = []        
    for objValue in objValuesNameList:
        if objValue.find('_') != 0:
            listAttrNames.append(objValue)
            listAttrValues.append(objOne.__getattribute__(objValue))

    
    class Out: pass   
    out = Out()
    out.listAttrNames = listAttrNames
    out.listAttrValues = listAttrValues    
    out.strListAttrNames = ", ".join(listAttrNames)
    out.strListAttrValues = "'" + "', '".join(map(str,listAttrValues)) + "'"   
#         out.strListAttrValues = "'" + "', '".join(listAttrValues) + "'"   
    return out


def toStr(objOne): 
    attribList = splitAttributes(objOne) # dir(objOne) #
#     logging.info( ' TemplateParams::__str__ attribList = ' + str(attribList))
    className = str(objOne.__class__)
    itemsList = map(lambda x, y: ' "' + str(x) + '"' + ': "' + str(y) + '" ', attribList.listAttrNames, attribList.listAttrValues) 
    objValuesNameList = '\n'+ className + ': { \n\t' + ', \n\t'.join(itemsList) + '\n}'
    return objValuesNameList



def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance


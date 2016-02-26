
import logging
import json

import tornado

# !!!!!!!!!!
# !!!!!!!!!!


import core.models

# from core.models import DataException
from core.models.user import User
from core.models.article import Article

# чето я по - ходу, подключится просто забыл, да?




def main():

    logging.info( 'insert one Article 1 = ')
    
#     anyRtf = b"""{\rtf1\adeflang1025\ansi\ansicpg1251\uc1\adeff31507\deff0\stshfdbch31506\stshfloch31506\stshfhich31506\stshfbi31507\deflang1049\deflangfe1049\themelang1049\themelangfe0\themelangcs0{\fonttbl{\f0\fbidi \froman\fcharset204\fprq2{\*\panose 02020603050405020304}Times New Roman;}{\f34\fbidi \froman\fcharset1\fprq2{\*\panose 02040503050406030204}Cambria Math;}
# {\f37\fbidi \fswiss\fcharset204\fprq2{\*\panose 020f0502020204030204}Calibri;}{\flomajor\f31500\fbidi \froman\fcharset204\fprq2{\*\panose 02020603050405020304}Times New Roman;}"""
    anyRtf = """
  2 werwerwerwer
(Если 'вы уже знакомы с основами концепции тестирования', то вы, 
возможно, захотите перейти сразу к список методов "утверждений" (assert methods).)

Фреймворк тестирования юнитов Python, иногда называемый “PyUnit”, 
является версией Python`а для JUnit от Kent Beck и Erich Gamma. JUnit, 
в свою очередь, является Java версией фреймворка тестирования от Kent’а для Smalltalk. 
Каждый из них является стандартом де факто для своего языка.

unittest поддерживает автоматизацию тестов, использование общего кода для настройки и завершения тестов, 
объединение тестов в коллекции и отделение тестов от фреймворка для вывода информации. 
Модуль unittest предоставляет классы, которые облегчают поддержку этих свойств для наборов тестов.

    """
    


    artInst = Article()
    
    artInst.article_id = 1
    artInst.user_id = 44
    artInst.article_title = 'To Flat! Autors new "Text!" bla-bla-bla = 12.01.2016 002'# + str(artInst.article_id)
#     ' To Flat! Autors new "Text!" bla-bla-bla = ' + str(artInst.article_id)
    artInst.article_rtf = str(artInst.article_id) + anyRtf + str(artInst.article_id)


    
    rez = artInst.save()
    if rez:
        logging.info( 'Saved OK!!!! rez  = ' + str(rez))

     


# Create demo in root window for testing.
if __name__ == '__main__':
    main()

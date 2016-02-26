
import logging
import json


# !!!!!!!!!!
# !!!!!!!!!!


import core.models

# from core.models import DataException
from core.models.user import User
from core.models.article import Article

# чето я по - ходу, подключится просто забыл, да?


def main():
    userLoc =  User()
#     logging.info('HomeHandler:: userLoc '+ json.dumps(userLoc))
#     logging.info('HomeHandler:: userLoc ')
#     logging.info( userLoc)
    
#     print (list(userLoc.__dict__ ))

#     userLoc.user_id = 1
    userLoc.user_login = 'login2'
    userLoc.user_pass = 'login2'
    userLoc.user_name  = 'MyName And SurName ewrwerwerw' 
    userLoc.user_role = 'admin'
    userLoc.user_phon = '1234-65432-4444' 
    userLoc.user_email = 'mail_0005@mail.com'
    userLoc.user_external = ''



    logging.info( 'insert 1 = ')
    
    try:
        userLoc.save()
    except Exception as err:
        logging.error( 'have Error = ' + str(err))


    logging.info( 'update 1 = ')

    userLoc.user_id = 1
    userLoc.user_login = 'login'
    userLoc.user_pass = 'login'
    userLoc.user_email = 'mail_0001@mail.com'
 
 
#  посмотреть что такое и как пользоваться "многоязычкой." 
#  и, что такое "юнитесты"
#  и после этого можно делать сттьи - добавить,исправить,сохранить (с версиями!!!!)
#   
 
     
#     try:
#         userLoc.save()
#     except Exception as err:
#         logging.error( 'have Error = ' + str(err))

    userloginLoad =  User()

    logging.info( 'login 1 = ')
    loginMailStr = '' 
    pwdStr = 'qwqwqw'
    try: 
        if userloginLoad.login(loginMailStr, pwdStr):
            logging.info( 'userloginLoad = '  + str (userloginLoad))
    except Exception as err:
        logging.error( 'have Error = ' + str(err))
    
    logging.info( 'login 2 = ')
    loginMailStr = 'login' 
    pwdStr = ''
    try: 
        if userloginLoad.login(loginMailStr, pwdStr):
            logging.info( 'userloginLoad = '  + str (userloginLoad))
    except Exception as err:
        logging.error( 'have Error = ' + str(err))
    
    logging.info( 'login 3 = ')
    loginMailStr = 'login' 
    pwdStr = 'qwqwqw'
    try: 
        if userloginLoad.login(loginMailStr, pwdStr):
            logging.info( 'userloginLoad = '  + str (userloginLoad))
    except Exception as err:
        logging.error( 'have Error = ' + str(err))

    logging.info( 'login 4 = ')
    loginMailStr = 'mail_0005@mail.com' 
    pwdStr = 'login2'
    try: 
        if userloginLoad.login(loginMailStr, pwdStr):
            logging.info( 'userloginLoad = '  + str (userloginLoad))
    except Exception as err:
        logging.error( 'have Error = ' + str(err))

    logging.info( 'login 5 = ')
    loginMailStr = 'login' 
    pwdStr = 'login'
    try: 
        if userloginLoad.login(loginMailStr, pwdStr):
            logging.info( 'userloginLoad = '  + str (userloginLoad))
    except Exception as err:
        logging.error( 'have Error = ' + str(err))


    userLoad = User()
    
    try: 
        userLoad.load(1)
        logging.info( 'userLoad (1) = ' )
        logging.info( userLoad )
    except Exception as err:
        logging.error( 'have Error = ' + str(err))
    
    try:
        userLoad.load(33)
        logging.info( 'userLoad (33) = ' )
        logging.info( userLoad )
    except Exception as err:
        logging.error( 'have Error = ' + str(err))
    
    try:
        usersObjList = userLoad.list()
        logging.info( '!!!! usersObjList = ' )
        for oneUser in usersObjList:
            logging.info( oneUser )
    except Exception as err:
        logging.error( 'have Error = ' + str(err))

 
#     article =  Article()
#     articles = article.list()
#     logging.info('HomeHandler:: articles ??? ')
#     logging.info('HomeHandler:: articles '+ json.dumps(articles))


# Create demo in root window for testing.
if __name__ == '__main__':
    main()

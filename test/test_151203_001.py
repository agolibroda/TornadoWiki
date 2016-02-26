
import logging
import json



class Model:

#     @property
    def __init__ (self):    
        logging.info('Model:: __init__:: make init ')
        self.db = pymysql.connect(
                                                host =      config.options.mysql_host, #'127.0.0.1', 
#                                                 port=   config.options.mysql_port, #3306, 
                                                user=       config.options.mysql_user, #'root', 
                                                passwd=     config.options.mysql_password, #'', 
                                                db=         config.options.mysql_db, #'blog'
                                                charset=    config.options.mysql_charset,
                                                cursorclass=pymysql.cursors.DictCursor
                                                )

#     def __del__(self):
#         self.db.close()
    
    
#     @property
    def db(self):
        return self.db


class User(Model):

    def __init__ (self): 
        logging.info('User:: __init__')
        Model.__init__(self)   

#         self.db = pymysql.connect(
#                                                 host =      config.options.mysql_host, #'127.0.0.1', 
# #                                                 port=   config.options.mysql_port, #3306, 
#                                                 user=       config.options.mysql_user, #'root', 
#                                                 passwd=     config.options.mysql_password, #'', 
#                                                 db=         config.options.mysql_db, #'blog'
#                                                 charset=    config.options.mysql_charset,
#                                                 cursorclass=pymysql.cursors.DictCursor
#                                                 )

        self.user_id = 0
        self.user_login = ''
        self.user_name  = '' 
        self.user_role = ''
        self.user_phon = '' 
        self.user_email = ''
        self.user_external = ''
 
    def get(self):
#     def get(self, userId):
#     def get(userId):
        userId = 1
        logging.info('User:: get:: userId '+ json.dumps(userId))
        cur = self.db.cursor()
        cur.execute("SELECT * FROM users WHERE id = %s", int(userId))
        sourse = cur.fetchall()
#         sourse = [{'user_id': 123}]
        logging.info('User:: get:: sourse '+ json.dumps(sourse))
 
       
#         for row in sourse:
#            print(row)
    
#         cur.close()
        return sourse
    
    def __str__(self): 
        return ('[User: %s, %s, %s, %s, %s, %s, %s]' % (self.user_id, self.user_login, self.user_name, self.user_role, self.user_phon, self.user_email, self.user_external))   



def main():
    user =  User()
    print('user')
    print(user)
#         logging.info('HomeHandler:: user '+ json.dumps(user))
#         logging.info('HomeHandler:: user '+ tornado.escape.json_encode(user))
    userId = 1
    entries = user.get() #userId)
    logging.info('HomeHandler:: entries ??? ')


# Create demo in root window for testing.
if __name__ == '__main__':
    main()

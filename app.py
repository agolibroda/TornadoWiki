#!/usr/bin/env python
#
# Copyright 2015 Alec Golibroda

# что нужно добавить до ядра ритона для нормальной работы
#
# easy_install pymysql - то же самое ??
# easy_install MySQL-python - не пошло!!!!!
# easy_install torndb 
# easy_install markdown
#


# import .BaseHandler
import logging
# import pickle
import json

import config

from core.UserControl import *
from core.ArticleControl import *
from core.AdminControl import *

from core.ProfileControl import *
from core.GroupControl import *

from core.RestControl import *



# from tornado.options import define, options



# A thread pool to be used for password hashing with bcrypt.
executor = concurrent.futures.ThreadPoolExecutor(2)



class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
            (r"/article/([^/]+)", ArticleHandler),
            (r"/compose", ComposeHandler),
            (r"/compose/([^/]+)", ComposeHandler),
            (r"/upload/([^/]+)",  UploadHandler), # upload #filesupl
            (r"/revisions", RevisionsHandler),
            (r"/revisionView", RevisionViewHandler),

            (r"/my_profile", MyProfileHandler),
            (r"/my_articles", MyArticletHandler),
            (r"/my_group", MyGroupHandler),
            
            (r"/articles", ArticleListHandler),
            
            (r"/groups", GroupsHandler),
            (r"/group/([^/]+)", GroupHandler),
            
            (r"/profiles", ProfilesHandler),
            (r"/profile/([^/]+)", ProfileHandler), 
            
            (r"/auth/create", AuthCreateHandler),
            (r"/auth/login", AuthLoginHandler),
            (r"/auth/logout", AuthLogoutHandler),


#             (config.options.adminPath, AdminHomeHandler, {"flag": "12345"}), # dict(flag=12345)
            (config.options.adminPath, AdminHomeHandler),
            (config.options.adminPath + r"/", AdminHomeHandler),
#             (config.options.adminPath + r"/articles", AdminFeedHandler),
#             (config.options.adminPath + r"/revisions", AdminRevisionsHandler),
#             (config.options.adminPath + r"/compose", AdminComposeHandler),
#             (config.options.adminPath + r"/revisionView", AdminRevisionViewHandler),
#             (config.options.adminPath + r"/article/([^/]+)", AdminArticleHandler),

# /rest/getArticleCategoryList 
            (r"/rest/([^/]+)/([0-9]+)",  RestMinHandler), # upload #filesupl

            (r"/([^/]+)", ArticleHandler), # Этим замыкаем список рутеров, так как он превнащает в название статьи ВСЕ!!!!
        
        ]
        settings = dict(
            wiki_title = "Tornado Wiki",
            wiki_title_admin ="Tornado Wiki Admin layer",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            ui_modules={
                        "Article": ArticleModule, 
                        'Revision': RevisionModule, 
                        "SimpleArticle": SimpleArticleModule,
                        'FilesList': FilesListModule,
                        },
            xsrf_cookies=True,
            cookie_secret= config.options.cookie_secret, #  "64d1c3defc5f9e829010881cfae22db38732",
            login_url="/auth/login",
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)
        # Have one global connection to the wiki DB across all handlers
        


def main():
    logging.info('config.options.main_port = ' + str(config.options.main_port))
    
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(config.options.main_port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()

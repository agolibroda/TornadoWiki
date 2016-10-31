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
from core.ProfileControl import *
from core.DeskTopControls import *

from core.GroupControl import *

from core.RestControl import *



# from tornado.options import define, options



# A thread pool to be used for password hashing with bcrypt.
executor = concurrent.futures.ThreadPoolExecutor(2)



class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),

            (r"/compose", ComposeHandler), # (ArticleControl) редактор - в зависимости от роли запускателя (или, откуда оно запускается?) такой набор инструментов и покажем.
            (r"/compose/([^/]+)", ComposeHandler), # (ArticleControl)
            (r"/upload/([^/]+)",  UploadHandler), # (ArticleControl) upload #filesupl

            (r"/revisions", RevisionsHandler),# (ArticleControl) Список ревизий как отдельный список (???) 
            (r"/revisionView", RevisionViewHandler), # (ArticleControl) просмотр одной рвизи????

            (r"/auth/create", AuthCreateHandler), # (ProfileControl.py)
            (r"/auth/login", AuthLoginHandler), # (ProfileControl.py)
            (r"/auth/logout", AuthLogoutHandler), # (ProfileControl.py)
            (r"/profile", MyProfileHandler), # (ProfileControl.py) мой собственный профиль - что бы поредактировать
            (r"/profile/([^/]+)", UserProfile), # (ProfileControl.py) профиль любого пользователя - по ИД - ну надо же поглядеть!

            (r"/perconalDeskTop", PerconalDeskTop), # (DeskTopControls) персональный рабочий стол пользователя - 
            (r"/groupDeskTop", GroupDeskTop), # (DeskTopControls) рабочий стол участника группы
            (r"/groupAdmDeskTop", GroupAdmDeskTop), # (DeskTopControls) РС Админа Группы
            (r"/sysAdmDeskTop", SysAdmDeskTop), # (DeskTopControls) РС Админа СИСТЕМЫ 

            (r"/rest/([^/]+)/([0-9]+)",  RestMinHandler), # (RestControl.py) все, что вызывается из клиента AJAX... 

            (r"/([^/]+)", ArticleHandler), # (ArticleControl) Этим замыкаем список рутеров, так как он превнащает в название статьи ВСЕ!!!!

# Это походу, надо вычистить - умерло.
#             (r"/article/([^/]+)", ArticleHandler),
#             (r"/my_articles", MyArticletHandler),
#             (r"/my_group", MyGroupHandler),
#             (r"/articles", ArticleListHandler),
#             (config.options.adminPath, AdminHomeHandler, {"flag": "12345"}), # dict(flag=12345)
#             (config.options.adminPath, AdminHomeHandler),
#             (config.options.adminPath + r"/", AdminHomeHandler),
#             (config.options.adminPath + r"/articles", AdminFeedHandler),
#             (config.options.adminPath + r"/revisions", AdminRevisionsHandler),
#             (config.options.adminPath + r"/compose", AdminComposeHandler),
#             (config.options.adminPath + r"/revisionView", AdminRevisionViewHandler),
#             (config.options.adminPath + r"/article/([^/]+)", AdminArticleHandler),

        
        ]
        settings = dict(
            wiki_title = "TorWiki",
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

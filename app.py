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

from core.BaseHandler import *

# from tornado.options import define, options



# A thread pool to be used for password hashing with bcrypt.
executor = concurrent.futures.ThreadPoolExecutor(2)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
            (r"/alter/", AlterHandler),
            (r"/archive", ArchiveHandler),
            (r"/feed", FeedHandler),
            (r"/article/([^/]+)", ArticleHandler),
            (r"/compose", ComposeHandler),
            (r"/revisions", RevisionsHandler),
            (r"/revisionView", RevisionViewHandler),
            (r"/upload/([^/]+)",  UploadHandler), # upload #filesupl
            
            (r"/auth/create", AuthCreateHandler),
            (r"/auth/login", AuthLoginHandler),
            (r"/auth/logout", AuthLogoutHandler),
        ]
        settings = dict(
            blog_title="Tornado Wiki",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            ui_modules={
                        "Article": ArticleModule, 
                        'Revision': RevisionModule, 
                        "SimpleArticle": SimpleArticleModule,
                        'FilesList': FilesListModule,
                        },
            xsrf_cookies=True,
            cookie_secret="64d1c3defc5f9e829010881cfae22db38732",
            login_url="/auth/login",
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)
        # Have one global connection to the wiki DB across all handlers
        


def main():
    logging.info('config.options.main_port')
    logging.info( str(config.options) )
#     pikky = pickle.dumps(config.options)

    pikky = json.dumps(config.options.mysql_db)
#     pikky = json.dumps({'foo': 'bar'})
    
    logging.info('config.options.main_port '+ pikky)
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(config.options.main_port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()

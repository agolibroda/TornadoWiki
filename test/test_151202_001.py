
import logging
import json


from core.models.user import User
from core.models.article import Article

def main():
    userLoc =  User()
    users = userLoc.list()
    logging.info('HomeHandler:: users ??? ')
    logging.info('HomeHandler:: users '+ json.dumps(users))

    article =  Article()
    articles = article.list()
    logging.info('HomeHandler:: articles ??? ')
    logging.info('HomeHandler:: articles '+ json.dumps(articles))


# Create demo in root window for testing.
if __name__ == '__main__':
    main()

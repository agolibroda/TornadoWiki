
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

    logging.info( 'select one Article 2 = ')
    
    

    artSel = Article()
   
    rezArtSel = artSel.list()
    logging.info( 'test_160104_002.py::: rezArtSel = ' + str(rezArtSel ) )
    for oneObj in rezArtSel:
        logging.info( 'test_160104_002.py::: oneObj = ' + str(oneObj))
    
  
#     try:
#         rezArtSel = artSel.load(findTitle)
#     
#         logging.info( 'rezArtSel = ' + str(rezArtSel ) )
# #         for oneRez in rezArtSel:
# #             logging.info( oneRez )
# 
#     except Exception as err:
#         logging.error( 'have Error = ' + str(err))
    

    
     
 

# Create demo in root window for testing.
if __name__ == '__main__':
    main()

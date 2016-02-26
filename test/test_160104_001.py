
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

    logging.info( 'select one Article 1 = ')
    
    


    artSel = Article()
    # to_flat!_autors_new_"text!"_bla-bla-bla_=_20
    # to_flat!_autors_new_"text!"_bla-bla-bla_=_10
    
    findTitle = 'to_flat!_autors_new_"text!"_bla-bla-bla_=_10'
  
    rezArtSel = artSel.load(findTitle)
    logging.info( 'rezArtSel = ' + str(rezArtSel ) )
  
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

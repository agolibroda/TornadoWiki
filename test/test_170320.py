
import logging

from string import Template



s = Template('$who likes $what')
logging.info( 'listByAutorId:: s = ' + str(s))
print (str(s))
#logging.info( 'listByAutorId:: substitute = ' + str(s.substitute(who='tim', what='kung pao')))
print (str(s.substitute(who='tim', what='kung pao')))

print (str(s.safe_substitute(who='tim', what='kung pao')))


strTpl = """
    SELECT 
    articles.article_id, articles.article_title, articles.article_link, articles.article_annotation, 
    articles.article_category_id, 
    articles.author_id,  articles.article_template_id, articles.article_permissions  
    FROM articles 
    WHERE  articles.author_id  = $aId 
    AND articles.article_permissions = 'pbl'
    UNION
    SELECT 
    articles.article_id, articles.article_title, articles.article_link, articles.article_annotation, 
    articles.article_category_id, 
    articles.author_id,  articles.article_template_id, articles.article_permissions  
    FROM articles, groups, librarys
    WHERE  articles.author_id  = $aId 
    AND articles.article_permissions = 'grp'
    AND groups.author_id = articles.author_id
    AND groups.author_id = $sId
    AND groups.group_id = librarys.group_id
    AND librarys.article_id = articles.article_id
    
    ORDER BY  article_id  
    
      """

tplWrk = Template(strTpl) # 
logging.info( 'listByAutorId:: 1 strTpl = ' + str(strTpl))
strOut  = tplWrk.safe_substitute(aId=str(123), sId=str(567))

print(strOut)

 
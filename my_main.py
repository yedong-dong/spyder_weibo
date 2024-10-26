from spyderComment import start as spiderCommentsStart
from spyContent import start as spiderContentStart
import warnings
warnings.filterwarnings('ignore')
import os
from sqlalchemy import create_engine
import pandas as pd

# engine=create_engine('mysql+pymysql://root:123456@localhost:3306/weiboyuqing?charset=utf8mb4')
#
# try:
#     with engine.connect() as connection:
#         print("数据库连接成功！")
# except Exception as e:
#     print(f"数据库连接失败: {e}")
#
# def save_to_sql():
#
#     try:
#         articleOldPd=pd.read_sql('select * from article',engine)
#         articleNewPd=pd.read_csv('navArticle.csv')
#         commentOldPd=pd.read_sql('select * from comments',engine)
#         commentNewPd=pd.read_csv('articleComment.csv')
#
#         concatArticlePd=pd.concat([articleOldPd,articleNewPd],join='inner')
#         concatCommentsPd=pd.concat([commentOldPd,commentNewPd],join='inner')
#
#         concatArticlePd.drop_duplicates(subset=['id'],keep='last',inplace=True)
#         concatCommentsPd.drop_duplicates(subset=['content'],keep='last',inplace=True)
#
#         concatArticlePd.to_sql('article',con=engine,if_exists='replace',index=False)
#         concatCommentsPd.to_sql('comments',con=engine,if_exists='replace',index=False)
#
#     except:
#         articleNewPd=pd.read_csv('navArticle.csv')
#         commentNewPd=pd.read_csv('articleComment.csv')
#         articleNewPd.to_sql('article', con=engine, if_exists='replace',index=False)
#         commentNewPd.to_sql('comments', con=engine, if_exists='replace',index=False)
#

def start():
    print("正在爬取内容")
    spiderContentStart(3,3)
    # print("正在爬取评论")
    # spiderCommentsStart()
    # print("正在保存")
    # save_to_sql()


if __name__ == '__main__':
    start()

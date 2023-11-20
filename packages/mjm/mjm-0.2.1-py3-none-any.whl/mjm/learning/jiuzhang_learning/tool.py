from lmf.dbv2 import db_query 
from sqlalchemy import create_engine,types
from sqlalchemy.dialects.postgresql import TEXT 
from sqlalchemy.dialects.postgresql import BIGINT
import pandas as pd 
import psycopg2,pg8000
def db_command(sql,dbtype='mssql',pool=0,conp=None):

    """db_command 仅仅到数据库"""
    if conp is None:conp=_pool[dbtype][pool]
    if dbtype=='postgresql':
        host=conp[2].split(":")[0]
        port="5432" if ':' not in conp[2] else conp[2].split(":")[1]
        con=pg8000.connect(user=conp[0], password=conp[1], host=host, port=port,database=conp[3])
    elif dbtype=='mssql':
        con=pymssql.connect(user=conp[0], password=conp[1], host=conp[2],database=conp[3])
    elif dbtype=='oracle':
        con = cx_Oracle.connect("%s/%s@%s/%s"%(conp[0],conp[1],conp[2],conp[3]))

    elif dbtype=='sqlite':
        con=sqlite3.connect(conp)
    else:
        host=conp[2].split(":")[0]
        port="3306" if ':' not in conp[2] else conp[2].split(":")[1]
        port=int(port)
        con = pymysql.connect(user=conp[0],passwd=conp[1],host=host,db=conp[3], port=port)
    
    cur=con.cursor()

    cur.execute(sql)
    con.commit()
    cur.close()
    con.close()

def db_command_ext(sql,dbtype='mssql',pool=0,conp=None):

    """db_command 仅仅到数据库"""
    if conp is None:conp=_pool[dbtype][pool]
    if dbtype=='postgresql':
        host=conp[2].split(":")[0]
        port="5432" if ':' not in conp[2] else conp[2].split(":")[1]
        con=pg8000.connect(user=conp[0], password=conp[1], host=host, port=port,database=conp[3])
        con.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    elif dbtype=='mssql':
        con=pymssql.connect(user=conp[0], password=conp[1], host=conp[2],database=conp[3])
    elif dbtype=='oracle':
        con = cx_Oracle.connect("%s/%s@%s/%s"%(conp[0],conp[1],conp[2],conp[3]))

    elif dbtype=='sqlite':
        con=sqlite3.connect(conp)
    else:
        host=conp[2].split(":")[0]
        port="3306" if ':' not in conp[2] else conp[2].split(":")[1]
        port=int(port)
        con = pymysql.connect(user=conp[0],passwd=conp[1],host=host,db=conp[3], port=port)
   
    cur=con.cursor()

    cur.execute(sql)
    con.commit()
    cur.close()
    con.close()

HOLO_CONP=["LTAI5tBUdQNg3AUjkauGi1fk","tZxt3S8dgtj7L0t1qEyDus7TxA7RLj","hgprecn-cn-m7r1sqd4u006-cn-shenzhen.hologres.aliyuncs.com:80","lebo","public"]
#HOLO_CONP=["LTAI5tBUdQNg3AUjkauGi1fk","tZxt3S8dgtj7L0t1qEyDus7TxA7RLj","hgprecn-cn-m7r1sqd4u006-cn-shenzhen-vpc.hologres.aliyuncs.com:80","lebo","public"]


PG_CONP=["postgres","since2015","1.12.63.208:5436","postgres","public"]

#PG_CONP=["postgres","since2015","127.0.0.1:5432","postgres","public"]


def holo_command(sql):
    conp=HOLO_CONP
    db_command(sql,dbtype="postgresql",conp=conp) 
def holo_command_ext(sql):
    conp=HOLO_CONP
    db_command_ext(sql,dbtype="postgresql",conp=conp) 

    

def holo_query(sql):
    conp=HOLO_CONP
    df=db_query(sql,dbtype="postgresql",conp=conp)
    return df 


def pg_command(sql):
    conp=PG_CONP
    db_command(sql,dbtype="postgresql",conp=conp) 
    
def pg_command_ext(sql):
    conp=PG_CONP
    db_command_ext(sql,dbtype="postgresql",conp=conp) 

    

def pg_query(sql):
    conp=PG_CONP
    df=db_query(sql,dbtype="postgresql",conp=conp)
    return df 



from datetime import datetime,timedelta

def get_delta_dates(bdate,edate,delta):
    data=[]

    if bdate==edate: return [(bdate,edate)]
    while bdate<edate:
        ldate=bdate
        rdate= datetime.strftime(datetime.strptime(bdate,'%Y%m%d')+timedelta(delta-1),'%Y%m%d' )
        bdate=datetime.strftime(datetime.strptime(bdate,'%Y%m%d')+timedelta(delta),'%Y%m%d' )
        data.append((ldate, min(rdate,edate)))
    if rdate<edate:
        data.append((bdate,edate))
    return data 

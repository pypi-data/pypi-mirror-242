#coding:utf-8
##@resource_reference{"pandas-1.3.0-cp37-cp37m-manylinux_2_5_x86_64.manylinux1_x86_64.zip"}
##@resource_reference{"psycopg2-2.9.6-cp37-cp37m-win_amd64.zip"}
# 导入模块

from datetime import datetime
import psycopg2
# from pygover.tool import db_query ,db_write,db_command


def conn_holo(host,port,dbname,user,password,application_name):
    conn = psycopg2.connect(host = host, port = port, dbname = dbname, user= user , password = password , application_name= application_name)
    return conn

def my_holo_query(sql,mode = "ddl"):
    
    host = "hgprecn-cn-m7r1sqd4u006-cn-shenzhen.hologres.aliyuncs.com"
    port = "80"
    dbname = "lebo"
    user = "LTAI5tDS41sByhnjCCMnz7ze"
    password = "6VcacaylxZyDVBowRH7Hj8N94pn4I4"
    application_name = "Python Test"
    conn = None
    cur = None
    df = None
    if mode == 'dql':
        conn = conn_holo(host,port,dbname,user,password,application_name)
        cur = conn.cursor() 
        cur.execute(sql)
        df = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
    else:
        conn = conn_holo(host,port,dbname,user,password,application_name)
        cur = conn.cursor() 
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
    return df

def query(p_date):
    sql_drop = f"""
        drop table if exists dm_ad.ods_ad_3rd_tag_package_detail_{p_date};
    """

    my_holo_query(sql_drop,mode = 'ddl')

    sql_create = f"""
        create table dm_ad.ods_ad_3rd_tag_package_detail_{p_date} partition of dm_ad.ods_ad_3rd_tag_package_detail for values in ('{p_date}');
    """

    my_holo_query(sql_create, mode ='ddl')

    sql_insert = f"""
        insert into dm_ad.ods_ad_3rd_tag_package_detail_{p_date}
        select *
        from dm_ad.ods_ad_3rd_tag_package_detail_ext 
        WHERE p_date = '{p_date}';
    """

    my_holo_query(sql_insert,mode = 'dml')
    sql_insert = f"""
        select  count(*) pv
        from    dm_ad.ods_ad_3rd_tag_package_detail
        where   p_date = '{p_date}'
    """

    df = my_holo_query(sql_insert,mode = 'dql')
    return df



if __name__ == '__main__':
    p_date = '20231119'
    rows = query(p_date)
    print('p_Date: %s' % p_date)
    for row in rows:
        print(row[0])



#coding:utf-8
##@resource_reference{"pandas-1.3.0-cp37-cp37m-manylinux_2_5_x86_64.manylinux1_x86_64.zip"}
##@resource_reference{"psycopg2-2.9.6-cp37-cp37m-win_amd64.zip"}
# 导入模块
from odps.udf import annotate
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
        drop table if exists tmp.temp_20231107_test;
    """

    my_holo_query(sql_drop,mode = 'ddl')

    sql_create = f"""
create table tmp.temp_20231107_test as

select  

        COALESCE (t1.platform,t2.platform) platform,

        COALESCE (t1.terminal,t2.terminal) terminal,

        coalesce(t1.app_version,t2.app_version) app_version,

        coalesce(t1.app_version_group,t2.app_version_group) app_version_group,

        coalesce(t1.is_new_version,t2.is_new_version) is_new_version,

        coalesce(t1.add_date,t2.add_date) add_date

from

(

SELECT  platform,terminal,app_version,app_version_group,is_new_version,add_date

FROM    app_conf.app_version_conf

) t1

full join

(

    select max(platform) platform,

        max(terminal) terminal,

        app_version,

        '其他' as app_version_group,

        '0' as is_new_version ,

        '20231106' as add_date

from jiuzhang.base

group by app_version

) t2

on t1.platform = t2.platform

and t1.terminal = t2.terminal

and t1.app_version = t2.app_version;

  

insert into app_conf.app_version_conf (platform,terminal,app_version,app_version_group,is_new_version,add_date) 

select platform,terminal,app_version,app_version_group,is_new_version,add_date

FROM tmp.temp_20231107_test

where add_date = '20231106';
    """

    my_holo_query(sql_create, mode ='ddl')
    print("1")
    # sql_insert = f"""
    #     insert into dm_ad.ods_ad_3rd_tag_package_detail_{p_date}
    #     select *
    #     from dm_ad.ods_ad_3rd_tag_package_detail_ext 
    #     WHERE p_date = '{p_date}';
    # """

    # my_holo_query(sql_insert,mode = 'dml')
    # sql_insert = f"""
    #     select  count(*) pv
    #     from    dm_ad.ods_ad_3rd_tag_package_detail
    #     where   p_date = '{p_date}'
    # """

    # df = my_holo_query(sql_insert,mode = 'dql')
    # return df



if __name__ == '__main__':
    p_date = '20231112'
    rows = query(p_date)
    # print('p_Date: %s' % p_date)
    # for row in rows:
    #     print(row[0])



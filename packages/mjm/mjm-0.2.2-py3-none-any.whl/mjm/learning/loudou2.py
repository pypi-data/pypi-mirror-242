

import pymysql
import json
md = pymysql.connect()
from dwsmc.tool import get_delta_dates,run_sql
from dwsmc.tool import query_sql
from datetime import datetime ,timedelta

def main2():
    create_table = """
    """
    sql = """
        select  coalesce(t1.p_date,t2.p_date,t3.p_date,t4.p_date)   p_date,
                t1.uv uv1,
                t2.uv uv2,
                t3.uv uv3,
                t4.uv uv4
        from   
        ( 
            (
                select  p_date,'t1' as A,count(distinct sdk_user_id) uv
                from    lebo_data.ods_sdk_event_input_detail
                where   1=1
                and     p_date >= '20230807' and p_date <= '20230809'
                and     service_type = 'app_init_result'
                and     init_type = '1'
                group by p_date 
            )   t1
            full join 
            (
                select  p_date,'t2' as A,count(distinct sdk_user_id) uv
                from    lebo_data.ods_sdk_event_input_detail
                where   1=1 
                and     p_date >= '20230808' and p_date <= '20230810'
                and     service_type = 'page_view'
                and     page_id = 'homepage'
                group by p_date
            )   t2
            on  t1.p_date = t2.p_date
            full join
            (
                select  p_date,'t3' as A,count(distinct case when lebo_data.appid2map(sdk_channel)['terminal'] = '发送端' then sdk_user_client_id
                                        when lebo_data.appid2map(sdk_channel)['terminal'] = '接收端' then sdk_user_receiver_id
                                        else nvl(sdk_user_client_id,sdk_user_receiver_id)
                                    end ) uv
                from    lebo_data.ods_sdk_mirror_detail
                where   1=1
                and     p_date >= '20230809' and p_date <= '20230811'
                and     service_number = '1'
                group by p_date
            )   t3
            on  coalesce(t1.p_date,t2.p_date) = t3.p_date
            full join
            (
                select  p_date,'t4' as A,count(distinct case when lebo_data.appid2map(sdk_channel)['terminal'] = '发送端' then sdk_user_client_id
                                        when lebo_data.appid2map(sdk_channel)['terminal'] = '接收端' then sdk_user_receiver_id
                                        else nvl(sdk_user_client_id,sdk_user_receiver_id)
                                    end ) uv
                from    lebo_data.ods_sdk_push_detail
                where   1=1
                and     p_date >= '20230810' and p_date <= '20230812'
                and     service_number = '1'
                group by p_date
            )   t4
            on  coalesce(t1.p_date,t2.p_date,t3.p_date) = t4.p_date 
        )
    """

    return sql

def rebuild():
    ddl_sql="""
        drop table if  exists lebo_data.dws_funnel_auto;
        create table if not exists lebo_data.dws_funnel_auto (
            p_date string,
            uv1 string,
            uv2 string,
            uv3 string,
            uv4 string
        ) ;
    """
    opt={ "odps.sql.submit.mode" : "script"}
    
    run_sql(ddl_sql,**opt)

def query():
    arr = query_sql("select * from lebo_data.dws_funnel_auto")
    print(arr)

def insert_sql(sql):
    insert_sql = f"""
        insert overwrite table lebo_data.dws_funnel_auto
        {sql}
    """
    opt={ "odps.sql.submit.mode" : "script"}
    print(insert_sql)
    run_sql(insert_sql,**opt)



if __name__ == '__main__':
    sql = main2()
    # insert_sql(sql)
    query()
    # rebuild()

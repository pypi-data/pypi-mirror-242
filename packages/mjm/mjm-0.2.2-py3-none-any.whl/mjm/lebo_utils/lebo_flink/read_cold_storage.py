
from pyflink.table import EnvironmentSettings, TableEnvironment
import sys 
import logging
import argparse
import importlib


def run_event_detail(parallelism='1'):
  env_settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
  table_env = TableEnvironment.create(environment_settings=env_settings) 
  # table_env.get_config().get_configuration().set_string('parallelism.default', parallelism)
  # table_env.get_config().get_configuration().setString("pipeline.classpaths", "D:\\flink\\usrlib\\ververica-connector-odps-1.13-vvr-4.0.15.jar")
  # 创建自定义函数
  # func_parse="f_parse"
  # for k,v in funcs.items():
  #     table_env.create_temporary_function(k,v)
  # for k,v in funcs.items():
  #   if "parse" in k: 
  #       func_parse=k
  #       break
  SQL_SRC=f"""
    create temporary table src(
        event_name  string ,
        table_name  string , 
        app_project_id string , 
        event_time_ms string , 
        lebo_uuid string , 
        sdk_user_id string , 
        custom string , 
        param string ,
        event_date string
  )
  with (
      'connector' = 'hologres'
      ,'dbname' = 'lebo'
      ,'tablename' = 'tmp.temp_jz_bi_specification_20230907'
      ,'username' = 'LTAI5tBUdQNg3AUjkauGi1fk'
      ,'password' = 'tZxt3S8dgtj7L0t1qEyDus7TxA7RLj'
      ,'endpoint' = 'hgprecn-cn-m7r1sqd4u006-cn-shenzhen.hologres.aliyuncs.com:80'
    )
    """


  SQL_DST=f"""
  create temporary table dst(
        
        event_name  string ,
        table_name  string , 
        hash_id bigint,
        idkey string,
        app_project_id string , 
        event_time_ms string , 
        lebo_uuid string , 
        sdk_user_id string , 
        custom string , 
        param string ,
        event_date string,
        json_params string,
        content string
  )
  with(
    'connector' = 'print'
  )
  """

  SQL_DST2 = """
    create temporary table dst(
        event_name  string ,
        table_name  string , 
        app_project_id string , 
        event_time_ms string , 
        lebo_uuid string , 
        sdk_user_id string , 
        custom string , 
        param string ,
        event_date string
  )
  with (
      'connector' = 'hologres'
      ,'dbname' = 'lebo'
      ,'tablename' = 'tmp.temp_jz_bi_specification_20230906'
      ,'username' = 'LTAI5tBUdQNg3AUjkauGi1fk'
      ,'password' = 'tZxt3S8dgtj7L0t1qEyDus7TxA7RLj'
      ,'endpoint' = 'hgprecn-cn-m7r1sqd4u006-cn-shenzhen.hologres.aliyuncs.com:80'
    )
  """

  SQL_INSERT=f"""
  insert into dst
  select 
        event_name,
        table_name   , 
        app_project_id  , 
        event_time_ms , 
        lebo_uuid , 
        sdk_user_id , 
        custom , 
        param ,
        event_date
   from src 
  """

  

  print(SQL_INSERT)
  table_env.execute_sql(SQL_SRC)
  table_env.execute_sql(SQL_DST2)
  table_env.execute_sql(SQL_INSERT).wait()



# def main(tp,f_parse_name,parallelism,net):
#     from lebo.common.dh1 import get_sub_bycomment
#     topic=f"lebo_data.src_{tp}_decode"
#     subid,starttime=get_sub_bycomment(topic,'dh2dh')
#     logging.info("start flink python")
#     print("start flink python")
#     logging.info(subid,starttime)
#     print(subid,starttime)
#     parallelism=str(parallelism)
#     dh2dh_prd(tp,subid,starttime,f_parse_name,parallelism=parallelism,net=net)


def main(parallelism = '1',net ='inner'):
    run_event_detail(parallelism='1')


if __name__=="__main__":
    print("start flink program")
    parser=argparse.ArgumentParser()
    parser.add_argument('--tp','-t',help="e mirror env push")
    parser.add_argument('--f_parse_name','-f',default='f_parse',help="e mirror env push")
    parser.add_argument('--parallelism','-p',default='1',help="e mirror env push")
    parser.add_argument('--net','-n',default='outer',help="e mirror env push")
    arg = parser.parse_args()
    main(arg.parallelism,arg.net)
from jiuzhang.tool import holo_query,holo_command
import json 
import datetime



# 分页获取监控规则
# def get_monitor_query_sql(param):
# pagenum = param['pagenum'] if 'pagenum' in param.keys() else 1
# pagesize = param['pagesize'] if 'pagesize' in param.keys() else 1000
# pagenum,pagesize=int(pagenum),int(pagesize)
# query_presql = f"""
#     select rule_id,
#             rule_name,
#             dev_mode,
#             monitor_type,
#             status,
#             create_time,
#             creater,
#             update_time
#             from tmp.rule_config
# """

# if pagenum != -1:
#     limitsql = f"\n order by update_time limit {pagesize} offset {(pagenum-1)*pagesize}"
# else:
#     limitsql = f"\n order by update_time "

# querysql = query_presql + limitsql
# df=holo_query(querysql)
# # 将timestamp格式转为字符串，json无法解析timestamp
# df['create_time'] = df['create_time'].astype(str)
# df['update_time'] = df['update_time'].astype(str)
# data=df.to_dict(orient='record')
# data=json.dumps(data,ensure_ascii=False)
# return data



#保存配置
def config_save_monitor1(param):
    name,env,monitor_type,status,userid,content = param['name'],param['env'],param['monitor_type'],param['status'],param['userid'],param['content']
    id = param['id'] if 'id' in param.keys() else None
    save_as_new=param['save_as_new'] if 'save_as_new' in param.keys() else False
    # insert
    if id is None or id == '':
        sql = f"""
            insert into jiuzhang.qual_user_config(name,env,monitor_type,status,create_time,update_time,userid,content)
            select 
                '{name}' as name,
                '{env}' as env ,
                '{monitor_type}' as monitor_type,
                '{status}' as status,
                current_date as create_time,
                current_date as update_time,
                '{userid}' as userid,
                            '{content}' as content;
            """
        print(sql)
    elif id is not None and save_as_new:
        sql = f"""
            insert into jiuzhang.qual_user_config(id,name,env,monitor_type,status,create_time,update_time,userid,content)
            select 
                '{id}' as id,
                 '{name}' as name,
                '{env}' as env ,
                '{monitor_type}' as monitor_type,
                '{status}' as status,
                current_date as  create_time,
                current_date as  update_time,
                '{userid}' as userid,
                            '{content}' as content;
        """
    else:
        sql = f"""
            update jiuzhang.qual_user_config set 
            name = '{name}',
            env = '{env}',
            monitor_type = '{monitor_type}',
            status = '{status}',
            update_time = CURRENT_TIMESTAMP,
            userid = '{userid}',
                    content = '{content}'
            where id = '{id}';
        """

    holo_command(sql)



# 根据规则名查询
def get_query_monitory(param):
    pass

cfg =  {
    "name": "TV端版本号格式校验",
    "env": "dev",
    "monitor_type": "single",
    "status": "0",
    "userid": "梅晓华",
    "content": "1"
}
# config_save_mc1(param)




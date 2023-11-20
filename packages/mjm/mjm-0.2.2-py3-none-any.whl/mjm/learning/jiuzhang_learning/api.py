from jiuzhang.tool import holo_query,holo_command
import json 
#1-事件选择
def get_event_enum():
    sql="""
    select 
    val,    
    coalesce(description,'') as description

    from jiuzhang.attr_value

    where colname='service_type' and val is not null 
    order by val desc 
    """
    df=holo_query(sql)
    data=df.to_dict(orient='record')
    data=json.dumps(data,ensure_ascii=False)
    return data


#2-口径选择
def get_cali_enum():
    sql="""
    with t as (select 
    show_name,
    json_agg( json_build_object('show_col_name',show_col_name,'col_name',col_name)) as val

    from jiuzhang.compute

    group by show_name)

    select *  from t  order by show_name
    """
    df=holo_query(sql)
    data=df.to_dict(orient='record')
    data=json.dumps(data,ensure_ascii=False)
    return data


# 3 运算符

def get_opt_enum():
    data=["=","!=","in","not in","为空","非空",">=",">","<","<="   ]
    data=json.dumps(data,ensure_ascii=False)
    return data

# 4 属性
def get_attr_enum():
    sql="""
    select 
    rawname,    
    coalesce(description,'') as description

    from jiuzhang.attrs

    where rawname is not null 

    """
    df=holo_query(sql)
    data=df.to_dict(orient='record')
    data=json.dumps(data,ensure_ascii=False)
    return data

# 5 属性val
def get_attr_val(val):
    sql=f"""
    select 
    val,
    coalesce(description,'') as description,

    coalesce(detail,'') as detail 

    from jiuzhang.attr_value

    where colname ='{val}'

    """
    df=holo_query(sql)
    data=df.to_dict(orient='record')
    data=json.dumps(data,ensure_ascii=False)
    return data


#6 分组

def get_group_enum():
    sql="""
    select 
    col_name as group,    
    coalesce(show_name,'') as description

    from jiuzhang.group

    where show_name is not null 

    """
    df=holo_query(sql)
    data=df.to_dict(orient='record')
    data=json.dumps(data,ensure_ascii=False)
    return data

## 7 获取周期

def get_period_enum():

    data=["小时","天","月","年","all"]
    data=json.dumps(data,ensure_ascii=False)
    return data


## 8 保存配置

def config_save_bk1(param):

    userid,name,content=param['userid'],param['name'],param['content']

    content=json.dumps(content,ensure_ascii=False)

    sql=f"""
    insert into jiuzhang.user_config(userid,name,content,create_time,update_time,ftype)
    select '{userid}' as userid,
    '{name}' as name,
    '{content}' as content 
    , CURRENT_TIMESTAMP as create_time
    , CURRENT_TIMESTAMP as update_time
    , {ftype} as ftype
    on conflict(userid,name)
    DO UPDATE SET
    userid=excluded.userid,
    name=excluded.name,
    content=excluded.content,
    update_time=excluded.update_time,
    ftype=excluded.ftype
    ;
    """

    holo_command(sql)

def config_save(param):

    userid,name,content,dash_type=param['userid'],param['name'],param['content'],param['dash_type']
    ftype=param['ftype'] if 'ftype' in param.keys() else '1'
    fid=param['id'] if 'id' in param.keys() else None
    save_as_new=param['save_as_new'] if 'save_as_new' in param.keys() else False
    content=json.dumps(content,ensure_ascii=False)

    if fid is None or fid=='':
        sql=f"""
        insert into jiuzhang.user_config(userid,dash_type,name,content,create_time,update_time,ftype)
        select 
        '{userid}' as userid,
        '{dash_type}' as dash_type,
        '{name}' as name,
        '{content}' as content 
        , CURRENT_TIMESTAMP as create_time
        , CURRENT_TIMESTAMP as update_time
        , {ftype} as ftype
        """
    elif save_as_new and fid is not None:
        sql=f"""
        insert into jiuzhang.user_config(userid,dash_type,name,content,create_time,update_time,ftype)
        select 
        '{userid}' as userid,
        '{dash_type}' as dash_type,
        '{name}' as name,
        '{content}' as content 
        , CURRENT_TIMESTAMP as create_time
        , CURRENT_TIMESTAMP as update_time
        , {ftype} as ftype
        ;
        """
    else:
        sql=f"""
        update  jiuzhang.user_config set 
        userid='{userid}',
        name='{name}',
        content='{content}',
        update_time=CURRENT_TIMESTAMP,
        ftype='{ftype}'
        where id={fid};
        """

    #print(sql)
    holo_command(sql)






def config_check(param):
    userid,name=param['userid'],param['name']
    sql=f"""select * from jiuzhang.user_config  where userid='{userid}'
    and name='{name}'
    """
    df=holo_query(sql)
 
    if not df.empty:
        tag={"msg":"exists"}
    else:
        tag={"msg":"not exists"}
    return tag 

def config_saved_list(userid,wd,dash_type,ftype,pagenum,pagesize):
    userid_str=f"and userid='{userid}' " if userid!='' else ''
    wd_str=f" and name ~'{wd}' " if wd!='' else ''
    dash_type_str=f" and dash_type='{dash_type}'"
    ftype_str=f" and ftype='{ftype}'" if ftype!='all' else ''

    sql=f"""
    with a as (
    select id,userid,dash_type,name,create_time::text create_time,update_time::text update_time  ,ftype
    ,count(1) over() as total
    from jiuzhang.user_config  
    where 1=1 
    {userid_str}
    {wd_str}
    {dash_type_str} 
    {ftype_str}
  )
    select * from a 
      order by update_time desc
    limit {pagesize} offset {(pagenum-1)*pagesize}
    """
    df=holo_query(sql)
    total=df.pop('total')
    if total.empty:
        total=0
    else:
        total=int(total.iat[0])
    data=df.to_dict(orient='record')
    result={"data":data,"total":total,"pagenum":pagenum,"pagesize":pagesize}
    result=json.dumps(result,ensure_ascii=False)
    return result


def config_query(id):

    sql=f"""select id,userid,dash_type,name,content,ftype from jiuzhang.user_config  where id={id}
    """
    df=holo_query(sql)
    data=df.to_dict(orient='record')
    if len(data)>=1:
        data=json.dumps(data[0],ensure_ascii=False)
    else:
        data={}
    return data



def config_delete(id):

    sql=f"""delete from jiuzhang.user_config  where id={id}
    """
    holo_command(sql)
    data={"msg":"success","id":id}
    return data


def test():
    return 'aaaaaaa'



# param={
#   "userid": "1634153714943258625",
#   "dash_type": "personal",
#   "name": "测试save接口4",
#   "id":386,
#   "save_as_new": False,
#   "content": {
#     "query_config": [
#       {
#         "name": "A",
#         "newName": "",
#         "event": "page_view_card_result",
#         "compute": [
#           "总人数",
#           "uid"
#         ],
#         "logic": "AND",
#         "filters": []
#       }
#     ],
#     "global_config": {
#       "filters": [],
#       "logic": "AND"
#     },
#     "groups": [],
#     "expression": [],
#     "datetime": {
#       "period": "天",
#       "begin": "20231008",
#       "end": "20231008",
#       "time": [
#         "20231008",
#         "20231008"
#       ]
#     }
#   },
#   "ftype": "1"
# }

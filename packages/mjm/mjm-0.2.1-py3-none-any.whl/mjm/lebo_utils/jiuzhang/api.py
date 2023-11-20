from jiuzhang.tool import holo_query,holo_command
import json 

#获取监控规则
def get_monitor_check():
    sql="""
    select 
    规则id,
    规则名,
    环境,
    监控类型,
    状态,
    最近更新时间,
    创建人,
    创建时间
    from jiuzhang.xxx

    """
    df=holo_query(sql)
    data=df.to_dict(orient='record')
    data=json.dumps(data,ensure_ascii=False)
    return data


#保存配置

def config_save_mc1(param):
    
    规则id,规则名称,环境,监控类型,状态,创建人=param['规则id'],param['规则名称'],param['环境'],param['监控类型'],param['状态'],param['创建人']
    fid=param['id'] if 'id' in param.keys() else None
    content=json.dumps(content,ensure_ascii=False)

    sql=f"""
    insert into jiuzhang.xxx(规则id,规则名称,环境,监控类型,状态,创建人)
    select '{规则id}' as 规则id,
    '{规则名称}' as 规则名称,
    '{环境}' as 环境 ,
    '{监控类型}' as 监控类型,
    '{状态}' as 状态,
    CURRENT_TIMESTAMP as 最近更新时间,
    '{创建人}' as 创建人,
    CURRENT_TIMESTAMP as 创建时间,
    on conflict(规则id)
    DO UPDATE SET
    规则id=excluded.规则id,
    规则名称=excluded.规则名称,
    环境=excluded.环境,
    监控类型=excluded.监控类型,
    状态=excluded.状态,
    创建人=exluded.创建人
    ;
    """

    holo_command(sql)

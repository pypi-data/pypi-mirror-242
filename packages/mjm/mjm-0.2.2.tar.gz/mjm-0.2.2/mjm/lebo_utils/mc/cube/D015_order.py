
from dwsmc.autosql.api import cube_dim,un_sql
from dwsmc.tool import get_delta_dates,run_sql
dm_trade_order_pay_stats_create="""
drop table if  exists lebo_data.dm_trade_order_pay_stats ;
CREATE TABLE IF NOT EXISTS lebo_data.dm_trade_order_pay_stats(
    pay_type STRING ,
    order_event_type STRING,
    appid STRING,
    appid_type STRING,
    appid_platform STRING,
    appid_terminal STRING,
    appid_name STRING,
    is_new_user STRING,
    media_id STRING,
    is_pay STRING,
    is_recharge_user STRING,
    goods_name string,
    mtype_name string,
    is_first_pay_by_count string,
    is_first_pay_by_day string,
    autorenewal string,
    is_first_month_autorenewal string,
    pay_uv BIGINT,
    refund_uv BIGINT,
    pay_sum DECIMAL(38,18),
    order_count_by_oidnum BIGINT,
    order_count_by_quantity BIGINT,
    refund_sum DECIMAL(38,18),
    refund_count_by_oidnum BIGINT,
    refund_count_by_quantity BIGINT,
    tag string
) 
partitioned by (
    p_date string
)
STORED AS ALIORC
;

"""


def get_stat_cube_sql(bdate,edate,delta=3):
    arr=[
        "天-支付类型-业务线-端-平台-是否支付",
        "天-业务线",
        "天-业务线-端-平台",
        "天-渠道号-端-平台-业务线-渠道名",
        "天-业务线-商品名称",
        "天-业务线-端-平台-商品名称",
        "天-渠道号-端-平台-业务线-渠道名-商品名称",
        "天-支付类型-业务线",
        "天-支付类型-业务线-端-平台",
        "天-付费类型-业务线",
        "天-付费类型-业务线-端-平台",
        "天-付费类型-业务线-是否新用户",
        "天-付费类型-业务线-端-平台-是否新用户",
        "天-付费类型-渠道号-端-平台-业务线-渠道名-是否新用户",
        "天-付费类型-业务线-媒资id",
        "天-付费类型-业务线-端-平台-媒资id",
        "天-付费类型-渠道号-端-平台-业务线-渠道名-媒资id",
        "天-付费类型-业务线-是否支付",
        "天-付费类型-业务线-端-平台-是否支付",
        "天-付费类型-渠道号-端-平台-业务线-渠道名-是否支付",
        "天-付费类型-业务线-用户类型(1:续费用户,0:回流用户)",
        "天-付费类型-渠道号-端-平台-业务线-渠道名-用户类型(1:续费用户,0:回流用户)",
        "天-付费类型-业务线-是否新用户-用户类型(1:续费用户,0:回流用户)",
        "天-付费类型-渠道号-端-平台-业务线-渠道名-是否新用户-用户类型(1:续费用户,0:回流用户)",
        "天-业务线-端-平台-商品类型",
        "天-业务线-是否新付费用户(次)",
        "天-业务线-是否新付费用户(天)",
        "天-业务线-端-平台-是否新付费用户(次)",
        "天-业务线-端-平台-是否新付费用户(天)",
        "天-渠道号-端-平台-业务线-渠道名-是否新付费用户(次)",
        "天-渠道号-端-平台-业务线-渠道名-是否新付费用户(天)",
        "天-渠道号-端-平台-业务线-渠道名-是否新付费用户(次)-用户类型(1:续费用户,0:回流用户)",
        "天-渠道号-端-平台-业务线-渠道名-是否新付费用户(天)-用户类型(1:续费用户,0:回流用户)",
        "天-端-平台-业务线-是否新签约",
        "天-渠道号-端-平台-业务线-渠道名-支付类型-是否新签约"
    ]

    m=cube_dim()
    m.td={
          "p_date":"天",
          "pay_type":"支付类型",
          "order_event_type":"付费类型",
          "appid":"渠道号",
          "appid_platform":"平台",
          "appid_terminal":"端",
          "appid_type":"业务线",
          "appid_name":"渠道名",
          "is_new_user":"是否新用户",
          "media_id":"媒资id",
          "is_pay":"是否支付",
          "is_recharge_user":"用户类型(1:续费用户,0:回流用户)",
          "goods_name":"商品名称",
          "mtype_name":"商品类型",
          "is_first_pay_by_count":"是否新付费用户(次)",
          "is_first_pay_by_day":"是否新付费用户(天)",
          "autorenewal":"是否自动续费",
          "is_first_month_autorenewal":"是否新签约",
          "isgive":"是否赠与",
          "register_date":"注册日期",
          "is_first_refund_by_day":"是否首次退款(天)",
          "is_vip":"是否会员"
        }

    m.brr=["p_date","pay_type","order_event_type","appid","appid_type","appid_platform","appid_terminal","appid_name","is_new_user","media_id","is_pay","is_recharge_user","goods_name","mtype_name","is_first_pay_by_count","is_first_pay_by_day","autorenewal","is_first_month_autorenewal"]
    dims=m.get_dims(arr)
    dims= '\n'.join([ "                     "+w for w in dims.split("\n")])


    pre_sql=f"""
    
    """

    param=f"""
cube: 
    - dws_order_user_uv.[p_date][pay_type][order_event_type][appid][appid_type][appid_platform][appid_terminal][appid_name][is_new_user][media_id][is_pay][is_recharge_user][goods_name][mtype_name][is_first_pay_by_count][is_first_pay_by_day][autorenewal][is_first_month_autorenewal].[pay_uv][refund_uv][pay_sum][order_count_by_oidnum][order_count_by_quantity][refund_sum][refund_count_by_oidnum][refund_count_by_quantity]:
       dim:
{dims}
       agg:
          - pay_uv: _size(lebo_data.uv1uion(pay_uv))
          - refund_uv: _size(lebo_data.uv1uion(refund_uv))
       delta: {delta}
output: 
   - dm_trade_order_pay_stats.[p_date][pay_type][order_event_type][appid][appid_type][appid_platform][appid_terminal][appid_name][is_new_user][media_id][is_pay][is_recharge_user][goods_name][mtype_name][is_first_pay_by_count][is_first_pay_by_day][autorenewal][is_first_month_autorenewal].[pay_uv][refund_uv][pay_sum][order_count_by_oidnum][order_count_by_quantity][refund_sum][refund_count_by_oidnum][refund_count_by_quantity]:
         update: insert
         pt: "p_date"
         dim_tag: tag
"""
    #print(param)
    opt="""
    """
    sql=un_sql(param,opt)

    sql=pre_sql+'\n'+sql
    return sql 

def run_create_sql(sql):
    opt={ 
    "odps.sql.submit.mode" : "script",
    "odps.sql.python.version":"cp37"
    }
    run_sql(sql,**opt)

def run_batch(bdate,edate,delta=1):
    import time 
    bg=time.time()
    arr=get_delta_dates(bdate,edate,delta)
    arr.sort(key=lambda x:x[0],reverse=True)
    opt={ 
    "odps.sql.submit.mode" : "script",
    "odps.sql.python.version":"cp37"
    }
    for bdate,edate in arr:
        print(bdate,edate)
        sql=get_stat_cube_sql(bdate,edate)
        run_sql(sql,**opt)
    ed=time.time()
    cost=int(ed-bg)
    print("totally cost %d s"%cost)


def run_base_thread(bdate,edate,delta,truncate=False):
    opt6={"odps.stage.mapper.split.size":10,
    "odps.sql.python.version":"cp37",
            #"odps.sql.executionengine.batch.rowcount":"1",
            #"odps.stage.mem":"12288"
            }

    from lmf.tool import mythread
    sql=get_stat_cube_sql(bdate,edate,delta)
    sqls=sql.split("--delta--\n")
    sql_pre=sqls[0]

    sqls_detal=sqls[1:-1]

    sql_insert=sqls[-1]
    if not truncate:
        run_sql(sql_pre,**opt6)
    else:
        sql_pre="""truncate table lebo_data.dws_startup_uv_tmp """
        run_sql(sql_pre)
    arr=sqls_detal
    def f(x):
        run_sql(x,**opt6)
    mythread(arr,f).run(5)
    run_sql(sql_insert)




if __name__=="__main__":
    run_create_sql(dm_trade_order_pay_stats_create)
    # sql=get_stat_cube_sql('20230725','20230725')
    # print(sql)
    run_base_thread('20231106','20231106',3)
    # run_with_log()
    pass
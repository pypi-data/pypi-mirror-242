
import pymysql
import json
md = pymysql.connect()


def conn_mysql():
    try:
        db = pymysql.connect(host = "127.0.0.1",port = 3306,user="root",password = "123456")
        print("数据库连接成功")
    except pymysql.Error as e:
        print("数据库连接失败" + str(e))
    return db

def query_sql(cursor,sql):
    cursor.execute(sql)
    results = cursor.fetchall()
    return results

def query_all_table(cursor):
    database_name = "funnel"

    project_name = "1"

    funnel_model_sql = f"""
        select *
        from    {database_name}.funnel_model;
    """

    funnel_project_k_info_sql = f"""
        select *
        from    {database_name}.funnel_project_k_info;
    """

    funnel_project_extend_sql = f"""
        select *
        from    {database_name}.funnel_project_extend;
    """

    funnel_project_link_sql = f"""
        select *
        from    {database_name}.funnel_project_link;
    """


    funnel_model_results = query_sql(cursor,funnel_model_sql)
    funnel_project_k_info = query_sql(cursor,funnel_project_k_info_sql)
    funnel_project_extend = query_sql(cursor,funnel_project_extend_sql)
    funnel_project_link = query_sql(cursor,funnel_project_link_sql)

    return funnel_model_results,funnel_project_k_info,funnel_project_extend,funnel_project_link

def get_demand():

    json = """
        {
        "project_id" : "1",
        "demand" : "['用户启动','用户注册']",
        "tag": "['天-端','天-平台']"
    }
    """
    return json

def main1():
    db = conn_mysql()
    cursor = db.cursor()
    
    funnel_model_results,funnel_project_k_info,funnel_project_extend,funnel_project_link = query_all_table(cursor)


    # print(funnel_model_results)
    # print(funnel_project_k_info)
    # print(funnel_project_extend)
    # print(funnel_project_link)
    # print(type(funnel_model_results))
    # print(funnel_model_results[0])

    # 前端传的线上数据
    json_online_str = get_demand()
    json_online = json.loads(json_online_str)
    demand_list_online = eval(json_online['demand']) # eval将字符串的list转成list
    
    # 前端线上数据和数据库里的配置进行一个左关联，如果右侧存在空的，则认为数据库没有配置全，返回左关联右侧不存在的左值，让配置全数据
    # [i[0] for i in funnel_model_results]这句话的意思是取表的第一列数据 ,funnel_model_results 是一个表，存放的是二维数组,funnel_model_result的第一列数据对应的是demand字段
    ddl_empty_list = [dlo for dlo in demand_list_online if dlo not in [i[0] for i in funnel_model_results]]
    if ddl_empty_list is not None and ddl_empty_list != list():
        print(f"not exists funnel_model 'model' columns info name {ddl_empty_list}")
    
    # 前端线上数据和数据库的配置进行一个右关联，获取数据库里的条件和表名信息这些固定配置
    funnel_model_online = [fmr for fmr in funnel_model_results if fmr[0] in demand_list_online]
    print(funnel_model_online)


    # 执行条件
    sql_list = []
    for fmo in funnel_model_online:
        # 按照|||分割条件，然后将其用and 拼接起来
        condition = [ "and " + i for i in fmo[2].split("|||")]
        condition = "\n".join(condition)
        sql = f"""
select *
from    lebo_data.{fmo[1]}
where   1=1 
{condition}
        """
        sql_list.append(sql)
    print(sql_list)
    db.close()

    


if __name__ == '__main__':
    pass
    # main1()
    # main2()
    






    




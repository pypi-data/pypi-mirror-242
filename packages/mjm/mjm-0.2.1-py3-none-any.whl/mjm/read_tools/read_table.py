#文件的读取
import os
#以相对路径打开文件


def read_data(file_name):
    f = open(file_name,encoding='utf-8')
    #以绝对路径打开文件
    #f= open("D:\\Anacond/work/learn数据清洗/文件读取及其处理/test.txt",encoding='utf-8')
    #读取文件
    arr = list()
    for r in f.readlines():
        arr.append(r.replace("\n",""))
    #关闭文件
    f.close()
    return arr

if __name__ == '__main__':
    arr = read_data("./input_data.txt")
    input_set = set()
    for a in arr:
        input_set.add(a)
    # print(input_set)
    database_dict = {'statistic_db':"jdbc:mysql://192.168.3.220:3306/statistic_db",'saas_cloud_lebox':"lebox",'youmi_rds_lbyun_mirror':"lbyun_mirror", 'ali_rds_dm_statistic':"db", 'lb_user_readonly':"dev_plat_boot", 'ali_dm_jdbc_49235910':"jdbc:mysql://rm-wz95c1geyub0ma49235910.mysql.rds.aliyuncs.com:3306/db", 'lbyun':"lbyun", 'dev_plat_boot':"jdbc:mysql://rr-wz939889pw1i9rx65.mysql.rds.aliyuncs.com:3306/dev_plat_boot", 'lbyun_use':"lbyun_user", 'saas_lebox_jdbc':"jdbc:mysql://rm-wz98i81uuomc7l755.mysql.rds.aliyuncs.com:3306/lebox", 'aliyun_statistic_conn':"statistic", 'ad_rds_682n72':"lebocloud_ad"}
    # for a in arr:
    #     print(f"{database_dict[a]}")
    for k,v in database_dict.items():
        print(v)
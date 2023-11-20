file_path = ['oss://bigdata-log-report/log/rp_nginx01/service/20230901/']
# for i in range(1,10):
#     file_name = "abc"+str(i)
#     file_path.append(file_name)
# print(file_path)


def create_sql():
  create_src_sql = []
  for i,element in enumerate(file_path):
    src_sql = f"""
        create temporary table src_{i}(
        `seg` VARCHAR
        )
        with (
      'connector' = 'filesystem',
      'path' = '{element}',
      'format' = 'raw'
    );


    create temporary view tmp_service_kafka_{i} as
    SELECT  
            trim(TRAILING ']' from trim(leading '[' from SPLIT_INDEX(seg,'^^A',0))) remote_addr,
            trim(TRAILING ']' from trim(leading '[' from SPLIT_INDEX(seg,'^^A',1))) `localtime`,
            trim(TRAILING ']' from trim(leading '[' from SPLIT_INDEX(seg,'^^A',2))) column3,
            trim(TRAILING ']' from trim(leading '[' from SPLIT_INDEX(seg,'^^A',3))) `status`,
            trim(TRAILING ']' from trim(leading '[' from SPLIT_INDEX(seg,'^^A',4))) agent,
            trim(TRAILING ']' from trim(leading '[' from SPLIT_INDEX(seg,'^^A',5))) column6,
            trim(TRAILING ']' from trim(leading '[' from SPLIT_INDEX(seg,'^^A',6))) http_x_forwarded_for,
            SPLIT_INDEX(trim(TRAILING ']' from trim(leading '[' from SPLIT_INDEX(seg,'^^A',2))),' ',0) `action`,
            SPLIT_INDEX(SPLIT_INDEX(trim(TRAILING ']' from trim(leading '[' from SPLIT_INDEX(seg,'^^A',2))),' ',1),'?',0) uri,
            SPLIT_INDEX(SPLIT_INDEX(trim(TRAILING ']' from trim(leading '[' from SPLIT_INDEX(seg,'^^A',2))),' ',1),'?',1) args,
            SPLIT_INDEX(trim(TRAILING ']' from trim(leading '[' from SPLIT_INDEX(seg,'^^A',2))),' ',2) column11,
            'rd.hpplay.cn' host
    FROM src_{i} ;
    """
    create_src_sql.append(src_sql)
  create_src_sql_str = '\n'.join(create_src_sql)

  dst_sql = """
  CREATE TEMPORARY TABLE dst_service_odps(
    k_offset  bigint,
    k_timestamp varchar,
    `uri` varchar,
    `host` varchar, 
    `remote_addr` varchar,
    `agent` varchar,
    `args` varchar, 
    `action` varchar,
    `http_x_forwarded_for` varchar,
    `localtime` varchar,
    body varchar,
    `status` varchar,
    p_date varchar
  ) with (
       'connector' = 'odps',
        'endpoint' = 'http://service.cn-shenzhen.maxcompute.aliyun-inc.com/api',
        'tunnelEndpoint' = 'http://dt.cn-shenzhen.maxcompute.aliyun-inc.com',
        'project' = 'lebo_data',
        'tablename' = 'src_service_kafka',
        'accessid' = 'LTAI4GLAUYbsDT6uzVpmcSeo',
        'accessKey' = 'bRBzwK0VpTM4XyzsP5nSSoqoh8HCIU',
        'partition' = 'p_date'
  );
  """

  BEGIN_STATEMENT_SET = "BEGIN STATEMENT SET;"

  insert_sql = []
  for i,element in enumerate(file_path):
      dml_sql = f"""
      insert into dst_service_odps
      select  0 k_offset,
              cast(now() as varchar) k_timestamp,
              uri,
              host,
              remote_addr,
              agent,  
              args, 
              `action`, 
              http_x_forwarded_for, 
              `localtime`,  
              '' body,  
              status, 
              DATE_FORMAT(`localtime`, 'yyyy/MM/dd HH:mm:ss', 'yyyyMMdd') p_date
      from    tmp_service_kafka_{i};
      """
      insert_sql.append(dml_sql)
  insert_sql = '\n'.join(insert_sql)

  END = "END;"


  output_sql = create_src_sql_str + '\n' + dst_sql + '\n' + BEGIN_STATEMENT_SET + '\n' + insert_sql + '\n' + END

  f = open("D:\workspace_python\my_utils\lebo_utils\lebo_flink\output1.txt", "w")
  # 将Hello World写入文件中
  f.write(output_sql)
  # 关闭文件对象
  f.close()
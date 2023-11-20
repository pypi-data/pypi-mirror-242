import json
import requests

# 获取jwtToken
def getJwtToken():

    url = "https://abi-in.lebo.cn/bi/aeolus/api/v3/openapi/jwtToken"

    headers = {
        "Cookie" : "sessionid=5floux1sgr6r2ztr6c56k2koh2m6gpvc",
        "Content-Type":"application/json"

    }

    data = {
        "metadata": {
            "clientId": "d12928762368dc5456a9768b63647e4b",
            "clientSecret": "3246b5a1b90364322258c74abef0ca64",
            "proxyUser": "maijiaming",
            "expire": 7200
        },
        "userPayload": {
            "somekey": ""
        }
    }

    response = requests.post(url, headers = headers ,json = data)
    # Unicode转中文
    # print(response.content.decode("unicode-escape"))

    response_json = response.json()
    jwtToken = ""
    try:
        jwtToken = response_json['data']['jwtToken']
    except Exception as e:
        print('Error:',e)
    return jwtToken


def create_dataset_api(jwtToken,data):
  url = f"https://abi-in.lebo.cn/bi/aeolus/api/v4/open/dataset"

  headers = {

        "app-id" : "5",
        "Content-Type":"application/json",
        "Authorization":f"Bearer {jwtToken}"
  }
  print(headers)

  response = requests.post(url, headers = headers ,data = data)
  # Unicode转中文
  print(response.content.decode("unicode-escape"))

def get_fields(src_kv):
  fields_list = list()
  for k,v in src_kv.items():
    fields = {
      'name':k,
      'alias':k,
      'type':v,
      'comment':None,
      'isSourceTableField':False,
      "prepType": v,
      "is_select": True,
      "isDynamicPartition": False,
      "isSupport": True
    }
    fields_list.append(fields)
  files = json.dumps(fields_list)
  return files

def get_match_schema(src_kv):
  match_schema_list = list()
  for k,v in src_kv.items():
    match_schema = {
      "name": k,
      "type": v,
      "upstreamField": k
    }
    match_schema_list.append(match_schema)
  match_schema = json.dumps(match_schema_list)
  return match_schema

def create_node_conf(src_kv,dbName,tbName,dataSourceType = "greenplum"):
  fields = get_fields(src_kv)
  match_schema = get_match_schema(src_kv)
  nodeConf = f"""
    [
      {{
        "tbId": "hologres//{dbName}//{tbName}",
        "nodeType": "table",
        "dataSourceType": "greenplum",
        "dataSourceId": 150,
        "clusterName": "hologres",
        "dbName": "{dbName}",
        "tbName": "{tbName}",
        "tableAlias": "{tbName}",
        "displayDbName": "{dbName}",
        "schemaName": "{tbName}",
        "schemaNameAlias": "",
        "query": "",
        "fullOption": true,
        "fields": {fields},
        "matchSchema": {match_schema},
        "params": {{
                "extractType": "{{\\"key\\":\\"full\\"}}"
                }},
        "partitionConfList": [],
        "tableRowFilter": {{}},
        "upstreamDataSourceId": 150,
        "nodeId": "7c561de1-7348-4fe1-b2ec-1eb33e0b2249"
      }}
    ]
  """
  return nodeConf


def create_dependency_conf():
  dependencyConf = f"""
    {{
        "dependencies": [],
        "dependencyMethod": 0,
        "earliestBackTime": null,
        "filterUnCompleteSensor": null,
        "isSelfDepend": false,
        "nodeDepStatus": 1,
        "nodeKey": "Load_6ce7d3121671521535200",
        "nodeName": "输出_db_name.table_name"
    }}
  """
  return dependencyConf

def create_base_conf(dataSetName):
  baseConf = f"""
    {{
      "dataSetName": "{dataSetName}",
      "appId": 5,
      "dataSetType": 22,
      "ownerEmailPrefix": "maijiaming",
      "demoUrl": "",
      "isAuthEnable": 0,
      "isIntelligentSyncEnable": 1,
      "connectionMode": 0,
      "syncMode": 0,
      "parentId": 0
    }}
  """
  return baseConf

def create_data_tag_conf():
  dataTagConf = f"""
    {{
      "dimTbNodes": []
    }}
  """
  return dataTagConf

def create_data_table_conf(ttl=7):
  dataTableConf = f"""
    {{
          "ttl": {ttl},
          "dataSourceId": 0,
          "driverName": "click_house",
          "createConf": {{}},
          "sampleRate": 1,
          "partitionFieldList": [
            {{
                      "name": "p_date",
                      "valueList": null
                    }}
          ],
          "chQueryParams": {{
                  "openStrongConsistencyCheck": false
                }},
          "clusterName": "hologres",
          "kafkaCluster": "hologres"
        }}
  """
  return dataTableConf



def create_dim_met_list(src_kv):
  mixorder = 1
  dim_met_list = list()
  default_dim_met = {
        "name": "p_date",
        "displayName": "p_date",
        "expr": "p_date",
        "descr": "p_date",
        "defaultType": "date",
        "castDataTypeName": None,
        "dimMetCategoryId": None,
        "editable": 0,
        "dimMetMixOrder": 0,
        "geoInfo": None,
        "visible": 1,
        "dimMetVariety": 1,
        "showExpr": 1,
        "isAutoAdd": 1,
        "mapType": 0,
        "dimMetOrder": 0,
        "groupType": 0
      }
  dim_met_list.append(default_dim_met)
  for k,v in src_kv.items():
    dim_met = {
              "name": k,
              "expr": k,
              "descr": None,
              "defaultType": v,
              "castDataTypeName": None,
              "dimMetCategoryId": None,
              "editable": 1,
              "dimMetMixOrder": mixorder,
              "geoInfo": None,
              "visible": 1,
              "dimMetVariety": 2,
              "showExpr": 1,
              "dimMetType": v,
              "mapType": 0,
              "dimMetOrder": mixorder,
              "groupType": 0
            }
    mixorder += 1
    dim_met_list.append(dim_met)
  dimMetList = json.dumps(dim_met_list)
  # dimMetList = """
  #       [
  #           {
  #             "name": "p_date",
  #             "displayName": "p_date",
  #             "expr": "p_date",
  #             "descr": "p_date",
  #             "defaultType": "date",
  #             "castDataTypeName": null,
  #             "dimMetCategoryId": null,
  #             "editable": 0,
  #             "dimMetMixOrder": 0,
  #             "geoInfo": null,
  #             "visible": 1,
  #             "dimMetVariety": 1,
  #             "showExpr": 1,
  #             "isAutoAdd": 1,
  #             "mapType": 0,
  #             "dimMetOrder": 0,
  #             "groupType": 0
  #           },
  #           {
  #             "name": "platform",
  #             "expr": "platform",
  #             "descr": null,
  #             "defaultType": "string",
  #             "castDataTypeName": null,
  #             "dimMetCategoryId": null,
  #             "editable": 1,
  #             "dimMetMixOrder": 1,
  #             "geoInfo": null,
  #             "visible": 1,
  #             "dimMetVariety": 2,
  #             "showExpr": 1,
  #             "dimMetType": "string",
  #             "mapType": 0,
  #             "dimMetOrder": 1,
  #             "groupType": 0
  #           },
  #           {
  #             "name": "terminal",
  #             "expr": "terminal",
  #             "descr": null,
  #             "defaultType": "string",
  #             "castDataTypeName": null,
  #             "dimMetCategoryId": null,
  #             "editable": 1,
  #             "dimMetMixOrder": 2,
  #             "geoInfo": null,
  #             "visible": 1,
  #             "dimMetVariety": 2,
  #             "showExpr": 1,
  #             "dimMetType": "string",
  #             "mapType": 0,
  #             "dimMetOrder": 2,
  #             "groupType": 0
  #           },
  #           {
  #             "name": "app_version",
  #             "expr": "app_version",
  #             "descr": null,
  #             "defaultType": "string",
  #             "castDataTypeName": null,
  #             "dimMetCategoryId": null,
  #             "editable": 1,
  #             "dimMetMixOrder": 3,
  #             "geoInfo": null,
  #             "visible": 1,
  #             "dimMetVariety": 2,
  #             "showExpr": 1,
  #             "dimMetType": "string",
  #             "mapType": 0,
  #             "dimMetOrder": 3,
  #             "groupType": 0
  #           },
  #           {
  #             "name": "app_version_group",
  #             "expr": "app_version_group",
  #             "descr": null,
  #             "defaultType": "string",
  #             "castDataTypeName": null,
  #             "dimMetCategoryId": null,
  #             "editable": 1,
  #             "dimMetMixOrder": 4,
  #             "geoInfo": null,
  #             "visible": 1,
  #             "dimMetVariety": 2,
  #             "showExpr": 1,
  #             "dimMetType": "string",
  #             "mapType": 0,
  #             "dimMetOrder": 4,
  #             "groupType": 0
  #           },
  #           {
  #             "name": "is_new_version",
  #             "expr": "is_new_version",
  #             "descr": null,
  #             "defaultType": "string",
  #             "castDataTypeName": null,
  #             "dimMetCategoryId": null,
  #             "editable": 1,
  #             "dimMetMixOrder": 5,
  #             "geoInfo": null,
  #             "visible": 1,
  #             "dimMetVariety": 2,
  #             "showExpr": 1,
  #             "dimMetType": "string",
  #             "mapType": 0,
  #             "dimMetOrder": 5,
  #             "groupType": 0
  #           },
  #           {
  #             "name": "id",
  #             "expr": "id",
  #             "descr": null,
  #             "defaultType": "int",
  #             "castDataTypeName": null,
  #             "dimMetCategoryId": null,
  #             "editable": 1,
  #             "dimMetMixOrder": 6,
  #             "geoInfo": null,
  #             "visible": 1,
  #             "dimMetVariety": 2,
  #             "showExpr": 1,
  #             "dimMetType": "int",
  #             "mapType": 1,
  #             "dimMetOrder": 6,
  #             "groupType": 0
  #           }
  #         ]
  # """
  return dimMetList

def create_sync_conf(frequency = 'daily',scheduleTime = "06:00"):
  sync_conf = f"""
  {{
      "syncType": 1,
      "scheduleConf": {{
            "frequency": "{frequency}",
            "scheduleDay": "0",
            "scheduleTime": "{scheduleTime}"
          }},
      "writePartition": 0,
      "backtrackingConf": {{
        "enable": 0,
        "dateRange": {{}}
      }},
      "uniqueIndexList": [
        "id"
      ],
      "doradoAutoDdl": 0,
      "yarnName": "offline",
      "doradoPriority": "normal",
      "dynamicPartitionMode": false,
      "paramsConfList": [
        {{
          "name": "tqs.query.auto.retry.enable",
          "value": "true"
        }}
      ],
      "monitorConf": {{
            "alarmRules": [
              {{
                "failedAlarmItems": [
                  {{
                    "item": "retry_failed"
                  }}
                ],
                "timeoutAlarmItems": [],
                "resultAlarmItems": [],
                "normalNoticeConf": [
                  {{
                    "noticeChannel": "lark",
                    "users": [
                      "maijiaming"
                    ]
                  }}
                ]
              }}
            ]
          }},
        "retryNum": 1,
        "retryInterval": 5
      }}
  """
  return sync_conf

def create_where_conf():
  whereConf = """
    {
      "requiredRowFilter": [],
      "nodeRowFilter": {}
    }
  """
  return whereConf

def create_link_conf():
  linkConf = """
    []
  """
  return linkConf

def create_dim_met_category_list():
    dimMetCategoryList = """
    []
    """
    return dimMetCategoryList
def create_label_conf():
  labelConf = """
    {}
  """
  return labelConf

def create_dataset(baseConf,nodeConf,dataTableConf,dimMetList,syncConf,whereConf,dependencyConf,dagTagConf,linkConf,dimMetCategoryList,labelConf):
  baseConf = json.loads(baseConf)
  nodeConf = json.loads(nodeConf)
  dataTableConf = json.loads(dataTableConf)
  dimMetList = json.loads(dimMetList)
  syncConf = json.loads(syncConf)
  whereConf = json.loads(whereConf)
  dependencyConf = json.loads(dependencyConf)
  dagTagConf = json.loads(dagTagConf)
  linkConf = json.loads(linkConf)
  dimMetCategoryList = json.loads(dimMetCategoryList)
  labelConf = json.loads(labelConf)
  ds_dict = dict()
  ds_dict.update({"baseConf":baseConf})
  ds_dict.update({"dimMetList":dimMetList})
  ds_dict.update({"dataTableConf":dataTableConf})
  ds_dict.update({"nodeConf":nodeConf})
  ds_dict.update({"syncConf":syncConf})
  ds_dict.update({"whereConf":whereConf})
  ds_dict.update({"dependencyConf":dependencyConf})
  ds_dict.update({"dagTagConf":dagTagConf})
  ds_dict.update({"linkConf":linkConf})
  ds_dict.update({"dimMetCategoryList":dimMetCategoryList})
  ds_dict.update({"labelConf":labelConf})
  ds_json = json.dumps(ds_dict)
  # print(ds_json)
  return ds_json

def dataset_run(dataSetName,src_kv_columns,src_schema,src_table_name):
  nodeConf = create_node_conf(src_kv_columns,src_schema,src_table_name)
  dependencyConf = create_dependency_conf()
  baseConf = create_base_conf(dataSetName)
  dataTableConf = create_data_table_conf(ttl = 7)
  syncConf = create_sync_conf()
  whereConf = create_where_conf()
  dimMetList = create_dim_met_list(src_kv_columns)
  dagTagConf = create_data_tag_conf()
  linkConf = create_link_conf()
  dimMetCategoryList = create_dim_met_category_list()
  labelConf = create_label_conf()
  ds_json = create_dataset(baseConf,nodeConf,dataTableConf,dimMetList,syncConf,whereConf,dependencyConf,dagTagConf,linkConf,dimMetCategoryList,labelConf)
  jwtToken = getJwtToken()
  create_dataset_api(jwtToken,ds_json)

def test_run1():
  dataSetName = "测试34"
  src_kv_columns = {
    'id':'int',
    'platform':'string',
    'terminal':'string',
    'app_version':'string',
    'app_version_group':'string',
    'is_new_version':'string',
    'add_date':'string'
  }
  src_schema = "app_conf"
  src_table_name = "funnel_params"
  dataset_run(dataSetName,src_kv_columns,src_schema,src_table_name)

def test_run2():
  pass
  dataSetName = "测试33"
  src_kv_columns = {
    'item_type':'string',
    'item_ddl':'string',
    'group_tag':'string',
    'pre_sql':'string',
    'where_cond' :'string',
    'map_v_ddl':'string',
    'cube_map_v_ddl':'string',
    'arr':'array<string>',
    'mark':'string'
  }
  src_schema = "app_conf"
  src_table_name = "funnel_params"
  nodeConf = create_node_conf(src_kv_columns,src_schema,src_table_name)
  dependencyConf = create_dependency_conf()
  baseConf = create_base_conf(dataSetName)
  dataTableConf = create_data_table_conf(ttl = 7)
  syncConf = create_sync_conf()
  whereConf = create_where_conf()
  dimMetList = create_dim_met_list(src_kv_columns)
  dagTagConf = create_data_tag_conf()
  linkConf = create_link_conf()
  dimMetCategoryList = create_dim_met_category_list()
  labelConf = create_label_conf()
  ds_json = create_dataset(baseConf,nodeConf,dataTableConf,dimMetList,syncConf,whereConf,dependencyConf,dagTagConf,linkConf,dimMetCategoryList,labelConf)
  jwtToken = getJwtToken()
  create_dataset_api(jwtToken,ds_json)
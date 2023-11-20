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


# 获取数据集所用数据源信息
def getDataSetInfo(datasetId):

    url = f"https://abi-in.lebo.cn/bi/aeolus/api/v3/open/openDataFactory/getDataModelInfo?dataSetId={datasetId}"


    headers = {
        "Cookie" : "session=eyJhZW9sdXNfdjFfbG9naW4iOiJtYWlqaWFtaW5nIn0.ZNh4bQ.YNTGYOOHj8QP1rqwAiPhRRTyoPI; sessionid=xmpfk0bs04ueccavus6xu142fop3gc65"
    }

    response = requests.get(url, headers = headers)
    # Unicode转中文
    print(response.content.decode("unicode-escape"))

def synchronizeDatasets(jwttoken,datasetid,startDate,endDate,maxParallelism=10):
    url = f"https://abi-in.lebo.cn/bi/aeolus/api/v4/open/dataset/{datasetid}/syncJob"
    print(url)
    headers = {
        "Cookie" : "sessionid=5floux1sgr6r2ztr6c56k2koh2m6gpvc",
        "Content-Type":"application/json",
        "Authorization":f"Bearer {jwttoken}"
    }
    print(headers)
    data = {
        "nodeId": "",
        "startDate": startDate,
        "endDate": endDate,
        "checkMinMax": True,
        "skipCheck": True,
        "isSpecifyQueue": True,
        "queueName": "root.oryx_aeolus_vip",
        "maxParallelism": maxParallelism
    }
    print(data)

    response = requests.post(url, headers = headers ,json = data)
    # Unicode转中文
    print(response.content.decode("unicode-escape"))

def sync_app_version_group():
    jwtToken = getJwtToken()
    # synchronizeDatasets(jwtToken,)

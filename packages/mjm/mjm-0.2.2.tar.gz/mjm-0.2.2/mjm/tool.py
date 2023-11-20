from odps import ODPS
from datetime import datetime,timedelta
from dwsmc.conf.param import (AK,SK,ODPS_PORJECT_ENDPOINT,
    ODPS_PORJECT)
def run_sql(sql,o=None,**kwarg):
    if o is None:
        o = ODPS(AK, SK, ODPS_PORJECT, ODPS_PORJECT_ENDPOINT)

    for sql in sql.split(";"):
        if len(sql.strip())>4:
            instance=o.run_sql(sql,hints=kwarg)
            print(sql)
            print(instance.get_logview_address())  
            instance.wait_for_success() 



def query_sql(sql,o=None,**kwarg):
    if o is None:
        o = ODPS(AK, SK, ODPS_PORJECT, ODPS_PORJECT_ENDPOINT)

    

    with o.execute_sql(sql,hints=kwarg).open_reader() as f:
        arr=f.read()
    arr=[ w.values for w in arr]
    return arr 


def get_delta_dates(bdate,edate,delta):
    data=[]

    if bdate==edate: return [(bdate,edate)]
    while bdate<edate:
        ldate=bdate
        rdate= datetime.strftime(datetime.strptime(bdate,'%Y%m%d')+timedelta(delta-1),'%Y%m%d' )
        bdate=datetime.strftime(datetime.strptime(bdate,'%Y%m%d')+timedelta(delta),'%Y%m%d' )
        data.append((ldate, min(rdate,edate)))
    if rdate<edate:
        data.append((bdate,edate))
    return data 

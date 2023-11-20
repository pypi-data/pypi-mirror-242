from py2neo import Graph,Node,Relationship,Subgraph
from py2neo.matching import *
import pandas as pd 

def toneo4j(df1,df2,nodelabel='segment_id',sgtag='g1',edgetag='from'):
    from py2neo import Graph,Node,Relationship,Subgraph

    g=Graph("neo4j://xxxx:xxxx",auth=("xxxx", "xxxx"))
    print('start wrting neo4j')
    sgtag=sgtag
    nodelabel=nodelabel
    g.run("match (n)  where n.sgtag='%s' detach delete n"%sgtag)

    nodes={}
    edge_list=[]
    for w in df1.to_dict(orient='records'):
        dt=w[nodelabel]
        if dt is None or str(dt)=='nan':dt='qita'
        w['sgtag']=sgtag
        node=Node(dt,**w)
        
        nodes[w['guid']]=node


    for w in df2.to_dict(orient='records'):
        src,dst=w.pop('src'),w.pop('dst')

        edge=Relationship(nodes[src],edgetag,nodes[dst] ,**w)

        edge_list.append(edge)
    node_list=list(nodes.values())

    bg=0
    step=10000
    ed=bg+step
    total=len(node_list)
    g.create(Subgraph(nodes=node_list[bg:ed]))
    print("%d-%d"%(bg,ed))
    while ed<total:
        bg,ed=ed,ed+step
        g.create(Subgraph(nodes=node_list[bg:ed]))
        print("%d-%d"%(bg,ed))
        

    bg=0
    step=10000
    ed=bg+step
    total=len(edge_list)
    g.create(Subgraph(relationships=edge_list[bg:ed]))
    print("%d-%d"%(bg,ed))
    while ed<total:
        bg,ed=ed,ed+step
        g.create(Subgraph(relationships=edge_list[bg:ed]))
        print("%d-%d"%(bg,ed))


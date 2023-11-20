

from neo4j import GraphDatabase
from py2neo import Graph,Node,Relationship,Subgraph
from py2neo.matching import *

def conn_graph(url,user,password):
    graph = Graph(url, auth=(user, password))
    return graph

class HelloWorldExample:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def print_greeting(self, message):
        with self.driver.session() as session:
            greeting = session.execute_write(self._create_and_return_greeting, message)
            print(greeting)

    @staticmethod
    def _create_and_return_greeting(tx, message):
        result = tx.run("CREATE (a:Greeting) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)", message=message)
        return result.single()[0]

# 打开数据库
def toneo4j_create_node(graph):
    a_dict = {'guid': 1, 'segment_id': 'A', 'name': 'Alice'}
    a = Node("Person",**a_dict)
    graph.create(a)

def toneo4j_delete_node(graph):
    graph.run("match (n)  where n.guid= 1 detach delete n")

def toneo4j_queryAllNode(graph):
    person_nodes = graph.nodes.match("Person")

    for person_node in person_nodes:
        print(person_node)

def demo1(graph):
    graph.run("match (n)  where n.name = 'Alice' detach delete n")
    graph.run("match (n)  where n.name = 'Bob' detach delete n")
    graph.run("match (n)  where n.name = 'Carol' detach delete n")
    a = Node("Person",name = "Alice")
    b = Node("Person",name = "Bob")
    c = Node("Person",name = "Carol")
    KNOWS = Relationship.type("KNOW")
    ab = KNOWS(a,b)
    ba = KNOWS(b,a)
    ac = KNOWS(a,c)
    ca = KNOWS(c,a)
    bc = KNOWS(b,c)
    cb = KNOWS(c,b)
    friends = ab | ba | ac | ca | bc | cb
    
    graph.create(friends)
    print(a.graph)
    print(a.identity)

def demo2(graph):
    a = Node("Person",name = "Alice")
    print(type(a))

def demo3(graph):
    a = Node("Person",name = "Ferriy")
    b = Node("Person",name = "Gark")
    edge=Relationship(nodes[src],edgetag,nodes[dst] ,**w)



if __name__ == "__main__":
    graph = conn_graph("neo4j://193.112.178.219:7687", "neo4j", "since2015")
    demo2(graph)

    # greeter = HelloWorldExample("neo4j://193.112.178.219:7687", "neo4j", "since2015")
    # greeter.print_greeting("hello, world")
    # greeter.close()
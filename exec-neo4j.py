from neo4j import GraphDatabase
import requests
import time

uri = "neo4j://127.0.0.1:7687"
ip = "192.168.56.101"
driver = GraphDatabase.driver(uri, auth=("neo4j", "stage"))

def create_nodes(tx):
    tx.run( '''
            WITH "http://192.168.56.101:5000/rest/hosts" AS url2
            CALL apoc.load.json(url2) YIELD value as hosts

            MERGE (host:HOST {id: hosts.mac, ip: hosts.ipAddresses})

            MERGE (host)-[:LINK {srcPort: 0, dstPort: hosts.locations[0].port, poids: 1}]->(device:Device {id: hosts.locations[0].elementId})

            MERGE (device)-[:LINK {srcPort: hosts.locations[0].port, dstPort: 0, poids: 1}]->(host)

            WITH "http://192.168.56.101:5000/rest/links" AS url
            CALL apoc.load.json(url) YIELD value as links

            MERGE (device:Device {id: links.dst.device})
            MERGE (device2:Device {id: links.src.device})

            MERGE (device)-[:LINK {srcPort: links.dst.port, dstPort: links.src.port, poids: 1}]->(device2)
            MERGE (device2)-[:LINK {srcPort: links.src.port, dstPort: links.dst.port, poids: 1}]->(device)
            ''')

def update_graph(tx):
    tx.run( '''
            MATCH (n) DETACH DELETE n

            WITH "hosts.txt" AS url2
            CALL apoc.load.json(url2) YIELD value as hosts

            MERGE (host:HOST {id: hosts.mac, ip: hosts.ipAddresses})

            MERGE (host)-[:LINK {srcPort: 0, dstPort: hosts.locations[0].port, poids: 1}]->(device:Device {id: hosts.locations[0].elementId})

            MERGE (device)-[:LINK {srcPort: hosts.locations[0].port, dstPort: 0, poids: 1}]->(host)

            WITH "links.txt" AS url
            CALL apoc.load.json(url) YIELD value as links

            MERGE (device:Device {id: links.dst.device})
            MERGE (device2:Device {id: links.src.device})

            MERGE (device)-[:LINK {srcPort: links.dst.port, dstPort: links.src.port, poids: 1}]->(device2)
            MERGE (device2)-[:LINK {srcPort: links.src.port, dstPort: links.dst.port, poids: 1}]->(device)
            ''')

def waitForResourceAvailable():
    while True:
        response = requests.get("http://"+ip+":8081/changes/links")
        if response.status_code == 404:
            time.sleep(1)
        elif response.status_code == 200:
            f = open("C:/Users/ludam/.Neo4jDesktop/relate-data/dbmss/dbms-39eb1f4e-5062-47e4-b530-8e38f5b1504c/import/links.txt", "w")
            f.write(response.text)
            f.close()
            response2 = requests.get("http://"+ip+":5000/rest/hosts")
            f2 = open("C:/Users/ludam/.Neo4jDesktop/relate-data/dbmss/dbms-39eb1f4e-5062-47e4-b530-8e38f5b1504c/import/hosts.txt", "w")
            f2.write(response2.text)
            f2.close()
            with driver.session() as session:
                session.write_transaction(update_graph)
            print("Topologie changée")

with driver.session() as session:
    session.write_transaction(create_nodes)

waitForResourceAvailable()


driver.close()
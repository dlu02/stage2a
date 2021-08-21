from neo4j import GraphDatabase

uri = "neo4j://127.0.0.1:7687"
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

with driver.session() as session:
    session.write_transaction(create_nodes)

with driver.session() as session:
    session.write_transaction(create_nodes)

driver.close()
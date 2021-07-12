import requests
from requests.auth import HTTPBasicAuth
import networkx as nx
import matplotlib.pyplot as plt
import time

print("Démarrage de l'application IPS, veuillez patienter.\n")
print("Vérification de la disponibilité de l'API Onos...\n")

# url = "http://192.168.1.154:5000/graphql"
# liens_query = {'query': "query{liens{src,dst}}"}
# devices_query = {'query': "query{devices{id}}"}
# host_query = {'query': "query{hosts{id,locations}}"}
# r_devices = requests.post(url, auth=HTTPBasicAuth('karaf','karaf'), data = devices_query).text
# r_hosts = requests.post(url, auth=HTTPBasicAuth('karaf','karaf'), data = host_query).text
# r_links = requests.post(url, auth=HTTPBasicAuth('karaf','karaf'), data = liens_query).text

# print(r_links)


# création du graphe de la topologie du réseau associé au contrôleur ONOS à partir de son adresse IP
def create_graph_from_topology(ip):
    # initialisation du graphe
    gr = nx.Graph()

    # requêtes au contrôleur ONOS
    url = "http://"+ip+":5000/graphql"
    liens_query = {'query': "query{liens{src,dst}}"}
    host_query = {'query': "query{hosts{id,locations}}"}
    r_hosts = requests.post(url, auth=HTTPBasicAuth('karaf','karaf'), data = host_query)
    r_links = requests.post(url, auth=HTTPBasicAuth('karaf','karaf'), data = liens_query)

    if (r_hosts.status_code != 200):
        return "Erreur sur la liste des hôtes."
    elif (r_links.status_code != 200):
        return "Erreur sur la liste des liens."
    else:
        host_list = r_hosts.json()['data']['hosts']
        link_list = r_links.json()['data']['liens']
        
        # for i in devices_list:
        #     gr.add_node(i['id'])
        
        for l in link_list:
            gr.add_edge(l['src']['device'],l['dst']['device'],orig=l['src']['port'],dest=l['dst']['port'])
        
        for h in host_list:
            gr.add_node(h['id'],id=h['id'])
            gr.add_edge(h['id'],h['locations'][0]["elementId"],orig=h['locations'][0]["port"])
        
        return gr

start = time.time()
gr = create_graph_from_topology("192.168.1.154")
r=nx.draw(gr, with_labels=True)

# test Dijkstra
# l = nx.shortest_path(gr,"26:C6:B1:E2:CB:1F/None","CE:51:C6:10:7E:D9/None")
# print(l)

plt.savefig("test-graphql.png")
end = time.time()
print(end - start)
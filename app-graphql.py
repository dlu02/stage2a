import requests
from requests.auth import HTTPBasicAuth
import networkx as nx
import matplotlib.pyplot as plt

print("Démarrage de l'application IPS, veuillez patienter.\n")
print("Vérification de la disponibilité de l'API Onos...\n")

# url = "http://192.168.1.154:5000/graphql?query="
# liens_query = url+"query{liens{src,dst}}"
# devices_query = url+"query{devices{id}}"
# host_query = url+"query{hosts{id}}"
# r_devices = requests.get(devices_query, auth=HTTPBasicAuth('karaf','karaf')).text
# r_hosts = requests.get(host_query, auth=HTTPBasicAuth('karaf','karaf')).text
# r_links = requests.get(liens_query, auth=HTTPBasicAuth('karaf','karaf')).text

# print(r_links)


# création du graphe de la topologie du réseau associé au contrôleur ONOS à partir de son adresse IP
def create_graph_from_topology(ip):
    # initialisation du graphe
    gr = nx.Graph()

    # requêtes au contrôleur ONOS
    url = "http://"+ip+":5000/graphql"
    liens_query = {'query': "query{liens{src,dst}}"}
    devices_query = {'query': "query{devices{id}}"}
    host_query = {'query': "query{hosts{id,locations}}"}
    r_devices = requests.post(url, auth=HTTPBasicAuth('karaf','karaf'), data = devices_query)
    r_hosts = requests.post(url, auth=HTTPBasicAuth('karaf','karaf'), data = host_query)
    r_links = requests.post(url, auth=HTTPBasicAuth('karaf','karaf'), data = liens_query)

    if (r_hosts.status_code != 200):
        return "Erreur sur la liste des hôtes."
    elif (r_links.status_code != 200):
        return "Erreur sur la liste des liens."
    elif (r_devices.status_code != 200):
        return "Erreur sur la liste des appareils."
    else:
        devices_list = r_devices.json()['data']['devices']
        host_list = r_hosts.json()['data']['hosts']
        link_list = r_links.json()['data']['liens']
        
        # for i in devices_list:
        #     gr.add_node(i['id'])
        
        for l in link_list:
            gr.add_edge(l['src'],l['dst'])
        
        for h in host_list:
            gr.add_node(h['id'],id=h['id'])
            gr.add_edge(h['id'],h['locations'][0],color='red')
        
        return gr

gr = create_graph_from_topology("192.168.1.154")
r=nx.draw(gr, with_labels=True)

# test Dijkstra
# l = nx.shortest_path(gr,"26:C6:B1:E2:CB:1F/None","CE:51:C6:10:7E:D9/None")
# print(l)


plt.savefig("test.png")
plt.show()
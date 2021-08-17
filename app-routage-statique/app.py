import requests
from requests.auth import HTTPBasicAuth
import networkx as nx
import matplotlib.pyplot as plt
import time

print("Démarrage de l'application IPS, veuillez patienter.\n")
print("Vérification de la disponibilité de l'API Onos...\n")

# response = requests.get("http://192.168.1.154:8181/onos/v1/devices", auth=HTTPBasicAuth('karaf','karaf'))

# if response.status_code!=200:
#     print("API ONOS non disponible. Veuillez vérifier votre contrôleur.")
# else:
#     devices_list = response.json()['devices']
#     r_host = requests.get("http://192.168.1.154:8181/onos/v1/hosts", auth=HTTPBasicAuth('karaf','karaf'))
#     r_link = requests.get("http://192.168.1.154:8181/onos/v1/links", auth=HTTPBasicAuth('karaf','karaf'))
#     if (r_host.status_code != 200):
#         print("Erreur sur la liste des hôtes.")
#     elif (r_link.status_code != 200):
#         print("Erreur sur la liste des liens.")
#     else:
#         host_list = r_host.json()['hosts']
#         link_list = r_link.json()['links']
        
#         print(link_list)

# création du graphe de la topologie du réseau associé au contrôleur ONOS à partir de son adresse IP
def create_graph_from_topology(ip):
    # initialisation du graphe
    gr = nx.Graph()

    # requêtes au contrôleur ONOS
    # r_devices = requests.get("http://"+ip+":8181/onos/v1/devices", auth=HTTPBasicAuth('karaf','karaf'))
    r_host = requests.get("http://"+ip+":8181/onos/v1/hosts", auth=HTTPBasicAuth('karaf','karaf'))
    r_link = requests.get("http://"+ip+":8181/onos/v1/links", auth=HTTPBasicAuth('karaf','karaf'))
    if (r_host.status_code != 200):
        return "Erreur sur la liste des hôtes."
    elif (r_link.status_code != 200):
        return "Erreur sur la liste des liens."
    # elif (r_devices.status_code != 200):
    #     return "Erreur sur la liste des appareils."
    else:
        # devices_list = r_devices.json()['devices']
        host_list = r_host.json()['hosts']
        link_list = r_link.json()['links']
        
        # for i in devices_list:
        #     gr.add_node(i['id'])
        
        for l in link_list:
            gr.add_edge(l['src']['device'],l['dst']['device'])
        
        for h in host_list:
            gr.add_node(h['id'],id=h['id'])
            gr.add_edge(h['id'],h['locations'][0]['elementId'],color='red')
        
        return gr

start = time.time()
gr = create_graph_from_topology("192.168.1.154")
r=nx.draw(gr, with_labels=True)

# test Dijkstra
# l = nx.shortest_path(gr,"26:C6:B1:E2:CB:1F/None","CE:51:C6:10:7E:D9/None")
# print(l)

plt.savefig("test.png")
end = time.time()
print(end - start)
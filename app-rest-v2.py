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
    # r_devices = requests.get("http://"+ip+":8181/onos/v1/devices", auth=HTTPBasicAuth('karaf','karaf'))
    r_host = requests.get("http://"+ip+":5000/hosts", auth=HTTPBasicAuth('karaf','karaf'))
    r_link = requests.get("http://"+ip+":5000/links", auth=HTTPBasicAuth('karaf','karaf'))
    if (r_host.status_code != 200):
        return "Erreur sur la liste des hôtes."
    elif (r_link.status_code != 200):
        return "Erreur sur la liste des liens."
    # elif (r_devices.status_code != 200):
    #     return "Erreur sur la liste des appareils."
    else:
        # devices_list = r_devices.json()['devices']
        host_list = r_host.json()
        link_list = r_link.json()
        
        # for i in devices_list:
        #     gr.add_node(i['id'])
        
        for l in link_list:
            gr.add_edge(l['src']['device'],l['dst']['device'],orig=l['src']['port'],dest=l['dst']['port'])
        
        for h in host_list:
            gr.add_node(h['id'],id=h['id'])
            gr.add_edge(h['id'],h['locations'][0]["elementId"],orig="host",dest=h['locations'][0]["port"])
        
        return gr

start = time.time()
gr = create_graph_from_topology("192.168.1.154")
r = nx.draw(gr, with_labels=True)
plt.savefig("test.png")
end = time.time()

print("La topologie du réseau a été générée. Temps de génération : ", end - start, " secondes\n")
while (1):
    orig = input("Veuillez entrer l'hôte d'origine.\n")
    if orig not in gr:
        print("Hôte inexistant. Veuillez réessayer.\n")
    else:
        break
while (1):
    dest = input("Veuillez entrer l'hôte de destination.\n")
    if dest not in gr:
        print("Hôte inexistant. Veuillez réessayer.\n")
    else:
        break

print("Exécution de Dijsktra... \n")
# test Dijkstra
l = nx.shortest_path(gr,orig,dest)
print("Voici le chemin le plus court : \n")
print(l)
print("\nInstallation des intents :")

liste_intent = []
fwd_orig = ("","")
fwd_dest = ("","")
for i in range(0,len(l)-1):
    port = gr.get_edge_data(l[i],l[i+1])
    if (port["orig"]=="host"):
        fwd_orig = (l[i+1],port["dest"])
    else:
        fwd_dest = (l[i],port["orig"])
        if (port["orig"]!="host"):
            liste_intent.append([fwd_orig,fwd_dest])
            fwd_orig = (l[i+1],port["dest"])
        else:
            fwd_orig = ("","")

print(liste_intent)
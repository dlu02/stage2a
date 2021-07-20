import requests
from requests.auth import HTTPBasicAuth
import networkx as nx
import matplotlib.pyplot as plt
import time
import itertools

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
    gr = nx.DiGraph()

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
        global host_list_mac
        host_list_mac = []
        host_list = r_host.json()
        link_list = r_link.json()
        
        for l in link_list:
            gr.add_edge(l['src']['device'],l['dst']['device'],orig=l['src']['port'],dest=l['dst']['port'])
            gr.add_edge(l['dst']['device'],l['src']['device'],orig=l['dst']['port'],dest=l['src']['port'])
        
        for h in host_list:
            gr.add_node(h['id'],id=h['id'])
            host_list_mac.append(h['id'])
            gr.add_edge(h['id'],h['locations'][0]["elementId"],orig="host",dest=h['locations'][0]["port"])
            gr.add_edge(h['locations'][0]["elementId"],h['id'],orig=h['locations'][0]["port"],dest="host")
        
        return gr

start = time.time()
gr = create_graph_from_topology("192.168.1.154")
r = nx.draw(gr, with_labels=True)
plt.savefig("test.png")


# print("La topologie du réseau a été générée. Temps de génération : ", end - start, " secondes\n")
# while (1):
#     orig = input("Veuillez entrer l'hôte d'origine.\n")
#     if orig not in gr:
#         print("Hôte inexistant. Veuillez réessayer.\n")
#     else:
#         break
# while (1):
#     dest = input("Veuillez entrer l'hôte de destination.\n")
#     if dest not in gr:
#         print("Hôte inexistant. Veuillez réessayer.\n")
#     else:
#         break

def install_intent(mac_o,mac_d,liste_chemin):
    l=liste_chemin
    fwd_orig = ("","")
    fwd_dest = ("","")
    mac_orig = mac_o.replace("/None","")
    mac_dest = mac_d.replace("/None","")
    for i in range(0,len(l)-1):
        if i==len(l)-2:
            port = gr.get_edge_data(l[i],l[i+1])
            fwd_dest = (l[i],port["orig"])
            intent_orig = fwd_orig[0]+"-"+fwd_orig[1]
            intent_dest = fwd_dest[0]+"-"+fwd_dest[1]
            r_intent = requests.get("http://192.168.1.154:5000/intent?orig="+intent_orig+"&dest="+intent_dest
            +"&macorig="+mac_orig+"&macdest="+mac_dest)
            r_intent_inv = requests.get("http://192.168.1.154:5000/intent?orig="+intent_dest+"&dest="+intent_orig
            +"&macorig="+mac_dest+"&macdest="+mac_orig)
            print([intent_orig,intent_dest])
            print([intent_dest,intent_orig])
        else:
            port = gr.get_edge_data(l[i],l[i+1])
            if (port["orig"]=="host"):
                fwd_orig = (l[i+1],port["dest"])
            else:
                fwd_dest = (l[i],port["orig"])
                if (port["orig"]!="host"):
                    intent_orig = fwd_orig[0]+"-"+fwd_orig[1]
                    intent_dest = fwd_dest[0]+"-"+fwd_dest[1]
                    r_intent = requests.get("http://192.168.1.154:5000/intent?orig="+intent_orig+"&dest="+intent_dest
                    +"&macorig="+mac_orig+"&macdest="+mac_dest)
                    r_intent_inv = requests.get("http://192.168.1.154:5000/intent?orig="+intent_dest+"&dest="+intent_orig
            +"&macorig="+mac_dest+"&macdest="+mac_orig)
                    print([intent_orig,intent_dest])
                    print([intent_dest,intent_orig])

                    fwd_orig = (l[i+1],port["dest"])
                else:
                    fwd_orig = ("","")
    return "Installation chemin : "+mac_orig+" -> "+mac_dest+" OK"

list_comb = list(itertools.combinations(host_list_mac, 2))
for comb in list_comb:
    # dijsktra
    chemin = nx.shortest_path(gr,comb[0],comb[1])

    status = install_intent(comb[0],comb[1],chemin)

end = time.time()

print("Temps total ", end - start, " secondes\n")

""" 
# print("Exécution de Dijsktra... \n")
# test Dijkstra
l = nx.shortest_path(gr,orig,dest)
# print("Voici le chemin le plus court : \n")
# print(l)

# print("\nInstallation des intents :")






 """
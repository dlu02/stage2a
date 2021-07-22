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
def create_graph_from_topology_re(ip):
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

def install_intent_re(mac_o,mac_d,liste_chemin):
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

                    fwd_orig = (l[i+1],port["dest"])
                else:
                    fwd_orig = ("","")
    return "Installation chemin : "+mac_orig+" -> "+mac_dest+" OK"

# création du graphe de la topologie du réseau associé au contrôleur ONOS à partir de son adresse IP
def create_graph_from_topology_gq(ip):
    # initialisation du graphe
    gr = nx.DiGraph()

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
        global host_list_mac
        host_list_mac = []
        host_list = r_hosts.json()['data']['hosts']
        link_list = r_links.json()['data']['liens']
        
        for l in link_list:
            gr.add_edge(l['src']['device'],l['dst']['device'],orig=l['src']['port'],dest=l['dst']['port'])
            gr.add_edge(l['dst']['device'],l['src']['device'],orig=l['dst']['port'],dest=l['src']['port'])
        
        for h in host_list:
            gr.add_node(h['id'],id=h['id'])
            host_list_mac.append(h['id'])
            gr.add_edge(h['id'],h['locations'][0]["elementId"],orig="host",dest=h['locations'][0]["port"])
            gr.add_edge(h['locations'][0]["elementId"],h['id'],orig=h['locations'][0]["port"],dest="host")
        
        return gr

def install_intent_gq(mac_o,mac_d,liste_chemin):
    l=liste_chemin
    fwd_orig = ("","")
    fwd_dest = ("","")
    mac_orig = mac_o.replace("/None","")
    mac_dest = mac_d.replace("/None","")
    string_mut="mutation { \n"
        

    for i in range(0,len(l)-1):
        if i==len(l)-2:
            port = gr.get_edge_data(l[i],l[i+1])
            fwd_dest = (l[i],port["orig"])
            intent_orig = fwd_orig[0]+"/"+fwd_orig[1]
            intent_dest = fwd_dest[0]+"/"+fwd_dest[1]
            string_mut += "r"+str(i)+": addIntent(intent_orig: \""+intent_orig+"\", mac_orig: \""+mac_orig+"\", intent_dest: \""+intent_dest+"\", mac_dest: \""+mac_dest+"\") { intent_orig, intent_dest }\n"
            string_mut += "s"+str(i)+": addIntent(intent_orig: \""+intent_dest+"\", mac_orig: \""+mac_dest+"\", intent_dest: \""+intent_orig+"\", mac_dest: \""+mac_orig+"\") { intent_orig, intent_dest }\n"
        else:
            port = gr.get_edge_data(l[i],l[i+1])
            if (port["orig"]=="host"):
                fwd_orig = (l[i+1],port["dest"])
            else:
                fwd_dest = (l[i],port["orig"])
                if (port["orig"]!="host"):
                    intent_orig = fwd_orig[0]+"/"+fwd_orig[1]
                    intent_dest = fwd_dest[0]+"/"+fwd_dest[1]

                    string_mut += "r"+str(i)+": addIntent(intent_orig: \""+intent_orig+"\", mac_orig: \""+mac_orig+"\", intent_dest: \""+intent_dest+"\", mac_dest: \""+mac_dest+"\") { intent_orig, intent_dest }\n"
                    string_mut += "s"+str(i)+": addIntent(intent_orig: \""+intent_dest+"\", mac_orig: \""+mac_dest+"\", intent_dest: \""+intent_orig+"\", mac_dest: \""+mac_orig+"\") { intent_orig, intent_dest }\n"

                    fwd_orig = (l[i+1],port["dest"])
                else:
                    fwd_orig = ("","")

    string_mut += "}"
    mutation_query = {'query': string_mut}
    query_gql = requests.post("http://192.168.1.154:5000/graphql", auth=HTTPBasicAuth('karaf','karaf'), data = mutation_query)
    return "ok"

res_re = []
res_gq = []
gr = create_graph_from_topology_gq("192.168.1.154")
gr2 = create_graph_from_topology_re("192.168.1.154")

for i in range(0,20):
    orig="FE:C0:52:12:92:33/None"
    dest="8E:FC:DE:BA:3B:4B/None"
    start = time.time()
    l = nx.shortest_path(gr,orig,dest)
    install_intent_re(orig,dest,l)
    end = time.time()
    res_re.append(end-start)

    start = time.time()
    m = nx.shortest_path(gr,orig,dest)
    install_intent_gq(orig,dest,l)
    end = time.time()
    res_gq.append(end-start)    

print(res_re)
print(res_gq)

plt.plot([k for k in range(0,20)], res_re, label='REST')
plt.plot([k for k in range(0,20)], res_gq, label='GraphQL')
plt.legend()
plt.xlabel("Itération")
plt.ylabel("Temps d'exécution en secondes")
plt.savefig("resultats.png")
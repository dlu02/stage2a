import requests
import networkx as nx
import matplotlib.pyplot as plt

print("Démarrage de l'application IPS-graphql, veuillez patienter.\n")
print("Vérification de la disponibilité de l'API Onos...\n")

ip = "192.168.56.101"
# création du graphe de la topologie du réseau associé au contrôleur ONOS à partir de son adresse IP
def create_graph_from_topology(ip):
    # initialisation du graphe
    gr = nx.DiGraph()

    # requêtes au contrôleur ONOS
    url = "http://"+ip+":5000/graphql"
    liens_query = {'query': "query{liens{src,dst}}"}
    host_query = {'query': "query{hosts{id,locations}}"}
    r_hosts = requests.post(url, data = host_query)
    r_links = requests.post(url, data = liens_query)
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
            l['src'] = eval(l['src'])
            l['dst'] = eval(l['dst'])
            gr.add_edge(l['src']['device'],l['dst']['device'],orig=l['src']['port'],dest=l['dst']['port'])
            gr.add_edge(l['dst']['device'],l['src']['device'],orig=l['dst']['port'],dest=l['src']['port'])
        
        for h in host_list:
            h['locations'] = list(eval(h['locations']))
            gr.add_node(h['id'],id=h['id'])
            host_list_mac.append(h['id'])
            gr.add_edge(h['id'],h['locations'][0]["elementId"],orig="host",dest=h['locations'][0]["port"])
            gr.add_edge(h['locations'][0]["elementId"],h['id'],orig=h['locations'][0]["port"],dest="host")
        
        return gr

def install_intent(gr_graphql,mac_o,mac_d,liste_chemin):
    l=liste_chemin
    fwd_orig = ("","")
    fwd_dest = ("","")
    mac_orig = mac_o.replace("/None","")
    mac_dest = mac_d.replace("/None","")
    liste_intents = []
    
    for i in range(0,len(l)-1):
        if i==len(l)-2:
            port = gr_graphql.get_edge_data(l[i],l[i+1])
            fwd_dest = (l[i],port["orig"])
            intent_orig = fwd_orig[0]+"/"+fwd_orig[1]
            intent_dest = fwd_dest[0]+"/"+fwd_dest[1]
            liste_intents.append("{intentOrig: \""+intent_orig+"\", macOrig: \""+mac_orig+"\", intentDest: \""+intent_dest+"\", macDest: \""+mac_dest+"\"}")
            liste_intents.append("{intentOrig: \""+intent_dest+"\", macOrig: \""+mac_dest+"\", intentDest: \""+intent_orig+"\", macDest: \""+mac_orig+"\"}")
        else:
            port = gr_graphql.get_edge_data(l[i],l[i+1])
            if (port["orig"]=="host"):
                fwd_orig = (l[i+1],port["dest"])
            else:
                fwd_dest = (l[i],port["orig"])
                if (port["orig"]!="host"):
                    intent_orig = fwd_orig[0]+"/"+fwd_orig[1]
                    intent_dest = fwd_dest[0]+"/"+fwd_dest[1]

                    liste_intents.append("{intentOrig: \""+intent_orig+"\", macOrig: \""+mac_orig+"\", intentDest: \""+intent_dest+"\", macDest: \""+mac_dest+"\"}")
                    liste_intents.append("{intentOrig: \""+intent_dest+"\", macOrig: \""+mac_dest+"\", intentDest: \""+intent_orig+"\", macDest: \""+mac_orig+"\"}")

                    fwd_orig = (l[i+1],port["dest"])
                else:
                    fwd_orig = ("","")
    
    string_mut ="mutation MyMutation { addIntent(intentList: "
    string_mut += "["+",".join(liste_intents)+"]) { ok } }"
    mutation_query = {'query': string_mut}

    query_gql = requests.post("http://"+ip+":5000/graphql", data = mutation_query)
    print(query_gql.content)

    return "Ok"


res = []
gr = create_graph_from_topology(ip)
r = nx.draw(gr, with_labels=True)
plt.savefig("test-graphql.png")

while (1):
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

    l = nx.shortest_path(gr,orig,dest)
    install_intent(gr,orig,dest,l)
    print("Installation intent entre "+orig+" et "+dest+" OK")
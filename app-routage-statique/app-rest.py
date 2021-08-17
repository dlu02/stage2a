import requests
import networkx as nx
import matplotlib.pyplot as plt

print("Démarrage de l'application IPS-graphql, veuillez patienter.\n")
print("Vérification de la disponibilité de l'API Onos...\n")

ip = "192.168.56.101"
# création du graphe de la topologie du réseau associé au contrôleur ONOS à partir de son adresse IP
def create_graph_from_topology(ip):
    global rest_req_size
    # initialisation du graphe
    gr = nx.DiGraph()

    # requêtes au contrôleur ONOS
    r_host = requests.get("http://"+ip+":5000/rest/hosts")
    r_link = requests.get("http://"+ip+":5000/rest/links")
    rest_req_size = len(r_host.content + r_link.content)
    if (r_host.status_code != 200):
        return "Erreur sur la liste des hôtes."
    elif (r_link.status_code != 200):
        return "Erreur sur la liste des liens."
    else:
        global host_list_mac_re
        host_list_mac_re = []
        host_list = r_host.json()
        link_list = r_link.json()
        
        for l in link_list:
            gr.add_edge(l['src']['device'],l['dst']['device'],orig=l['src']['port'],dest=l['dst']['port'])
            gr.add_edge(l['dst']['device'],l['src']['device'],orig=l['dst']['port'],dest=l['src']['port'])
        
        for h in host_list:
            gr.add_node(h['id'],id=h['id'])
            host_list_mac_re.append(h['id'])
            gr.add_edge(h['id'],h['locations'][0]["elementId"],orig="host",dest=h['locations'][0]["port"])
            gr.add_edge(h['locations'][0]["elementId"],h['id'],orig=h['locations'][0]["port"],dest="host")
        
        return gr

def install_intent(gr_rest,mac_o,mac_d,liste_chemin):
    global size_req_re
    
    l=liste_chemin
    fwd_orig = ("","")
    fwd_dest = ("","")
    mac_orig = mac_o.replace("/None","")
    mac_dest = mac_d.replace("/None","")
    for i in range(0,len(l)-1):
        if i==len(l)-2:
            port = gr_rest.get_edge_data(l[i],l[i+1])
            fwd_dest = (l[i],port["orig"])
            intent_orig = fwd_orig[0]+"-"+fwd_orig[1]
            intent_dest = fwd_dest[0]+"-"+fwd_dest[1]
            
            r_intent = requests.get("http://"+ip+":5000/rest/intent?orig="+intent_orig+"&dest="+intent_dest
            +"&macorig="+mac_orig+"&macdest="+mac_dest)
            r_intent_inv = requests.get("http://"+ip+":5000/rest/intent?orig="+intent_dest+"&dest="+intent_orig
            +"&macorig="+mac_dest+"&macdest="+mac_orig)


        else:
            port = gr_rest.get_edge_data(l[i],l[i+1])
            if (port["orig"]=="host"):
                fwd_orig = (l[i+1],port["dest"])
            else:
                fwd_dest = (l[i],port["orig"])
                if (port["orig"]!="host"):
                    intent_orig = fwd_orig[0]+"-"+fwd_orig[1]
                    intent_dest = fwd_dest[0]+"-"+fwd_dest[1]
                    
                    r_intent = requests.get("http://"+ip+":5000/rest/intent?orig="+intent_orig+"&dest="+intent_dest
                    +"&macorig="+mac_orig+"&macdest="+mac_dest)
                    r_intent_inv = requests.get("http://"+ip+":5000/rest/intent?orig="+intent_dest+"&dest="+intent_orig
                    +"&macorig="+mac_dest+"&macdest="+mac_orig)


                    fwd_orig = (l[i+1],port["dest"])
                else:
                    fwd_orig = ("","")
    return "Ok"

res = []
gr = create_graph_from_topology(ip)
r = nx.draw(gr, with_labels=True)
plt.savefig("test-rest.png")

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
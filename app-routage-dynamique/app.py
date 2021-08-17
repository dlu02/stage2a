import requests
import networkx as nx
import time
import itertools
from multiprocessing import Process,freeze_support
import csv

ip = "192.168.56.101"
def create_graph_rest(ip):
    # initialisation du graphe
    gr = nx.DiGraph()

    # requêtes au contrôleur ONOS
    r_host = requests.get("http://"+ip+":5000/rest/hosts")
    r_link = requests.get("http://"+ip+":5000/rest/links")
    if (r_host.status_code != 200):
        return "Erreur sur la liste des hôtes."
    elif (r_link.status_code != 200):
        return "Erreur sur la liste des liens."
    else:
        global host_list
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
        
        return (gr,host_list_mac_re)

def waitForResourceAvailable():
    response = requests.get("http://"+ip+":8081/changes/links")
    while response.status_code == 404:
        time.sleep(1)
        if response.status_code == 200:
            break

def install_intent_re(gr_rest,mac_o,mac_d,liste_chemin):
    
    l=liste_chemin
    fwd_orig = ("","")
    fwd_dest = ("","")
    mac_orig = mac_o.replace("/None","")
    mac_dest = mac_d.replace("/None","")
    for i in range(0,len(l)-1):
        port = gr_rest.get_edge_data(l[i],l[i+1])
        if (port["orig"]=="host"):
            fwd_orig = (l[i+1],port["dest"])
        else:
            fwd_dest = (l[i],port["orig"])
            if (port["orig"]!="host"):
                intent_orig = fwd_orig[0]+"-"+fwd_orig[1]
                intent_dest = fwd_dest[0]+"-"+fwd_dest[1]
                    
                r_intent = requests.get("http://"+ip+":5000/rest/intent?orig="+intent_orig+"&dest="+intent_dest+"&macorig="+mac_orig+"&macdest="+mac_dest)
                r_intent_inv = requests.get("http://"+ip+":5000/rest/intent?orig="+intent_dest+"&dest="+intent_orig+"&macorig="+mac_dest+"&macdest="+mac_orig)

                fwd_orig = (l[i+1],port["dest"])
            else:
                fwd_orig = ("","")
    return "OK"


# création du graphe initial
l = create_graph_rest(ip)
gr = l[0]
host_l = l[1]

# liste des combinaisons d'hôtes à relier
liste_couples = list(itertools.combinations(host_l, 2))

# création de tous les chemins par dijkstra
res = []
for elt in liste_couples:
    res.append(nx.shortest_path(gr,elt[0],elt[1]))

def update():
    while True:
        response = requests.get("http://"+ip+":8081/changes/links")
        if response.status_code == 200:
            gr = nx.DiGraph()
            host_list_mac_re = []
            link_list = response.json()
        
            for l in link_list:
                gr.add_edge(l['src']['device'],l['dst']['device'],orig=l['src']['port'],dest=l['dst']['port'])
                gr.add_edge(l['dst']['device'],l['src']['device'],orig=l['dst']['port'],dest=l['src']['port'])
        
            for h in host_list:
                gr.add_node(h['id'],id=h['id'])
                host_list_mac_re.append(h['id'])
                gr.add_edge(h['id'],h['locations'][0]["elementId"],orig="host",dest=h['locations'][0]["port"])
                gr.add_edge(h['locations'][0]["elementId"],h['id'],orig=h['locations'][0]["port"],dest="host")
        
            l = (gr,host_list_mac_re)
            gr = l[0]
            host_l = l[1]

            # liste des combinaisons d'hôtes à relier
            liste_couples = list(itertools.combinations(host_l, 2))

            # création de tous les chemins par dijkstra
            res = []
            for elt in liste_couples:
                try:
                    res.append(nx.shortest_path(gr,elt[0],elt[1]))
                    break 
                except nx.exception.NetworkXNoPath:
                    res.append("NO")
                    print("Pas de chemin possible entre %s et %s" % elt)
            print(res)
            print("Mise à jour de la topologie suite à un changement.")
            print("Recalcul des intents actuels")

            f = open('intents.txt',newline='')
            reader = csv.reader(f)
            intents_installes = [tuple(row) for row in reader]
            print(intents_installes)
            for elt in intents_installes:
                (init,dest) = elt 
                if (init,dest) in liste_couples:
                    try:
                        chemin = nx.shortest_path(gr,elt[0],elt[1])
                        install_intent_re(gr,init,dest,chemin)
                        print("Hôtes %s et %s correctement reliés !" % (init,dest))
                        break 
                    except nx.exception.NetworkXNoPath:
                        print("Pas de chemin possible entre %s et %s" % elt)
                elif (dest,init) in liste_couples:
                    try:
                        chemin = nx.shortest_path(gr,elt[1],elt[0])
                        install_intent_re(gr,dest,init,chemin)
                        print("Hôtes %s et %s correctement reliés !" % (dest,init))
                        break 
                    except nx.exception.NetworkXNoPath:
                        print("Pas de chemin possible entre %s et %s" % elt)
        else:
            time.sleep(1)
    
def start():
    # création du graphe initial
    global l
    l = create_graph_rest(ip)
    gr = l[0]
    host_l = l[1]

    # liste des combinaisons d'hôtes à relier
    liste_couples = list(itertools.combinations(host_l, 2))

    # création de tous les chemins par dijkstra
    res = []
    for elt in liste_couples:
        res.append(nx.shortest_path(gr,elt[0],elt[1]))


if __name__ == '__main__':
    freeze_support()
    proc2 = Process(target=update)
    proc2.start()

    while True:
        init = input("Hôte d'origine : \n")
        dest = input("Hôte de destination : \n")
        if (init,dest) in liste_couples:
            l = (init, dest)
            index = liste_couples.index(l)
            chemin = res[index]
            install_intent_re(gr,init,dest,chemin)
            print("Hôtes %s et %s correctement reliés !" % (init,dest))
            f = open("intents.txt", "a")
            f.write(init+","+dest+"\n")
            f.close()
        elif (dest,init) in liste_couples:
            l = (dest, init)
            index = liste_couples.index(l)
            chemin = res[index]
            install_intent_re(gr,dest,init,chemin)
            print("Hôtes %s et %s correctement reliés !" % (dest,init))
            f = open("intents.txt", "a")
            f.write(init+","+dest+"\n")
            f.close()
        else:
            print("Couple absent !")
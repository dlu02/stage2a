#!/usr/bin/python
"""
Custom topology for Mininet, generated by GraphML-Topo-to-Mininet-Network-Generator.
"""
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.node import Node
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.util import dumpNodeConnections
class GeneratedTopo( Topo ):
    "Internet Topology Zoo Specimen."
    def __init__( self, **opts ):
        "Create a topology."
        # Initialize Topology
        Topo.__init__( self, **opts )

        # add nodes, switches first...
        Zurich = self.addSwitch( 's0' )
        Geneva = self.addSwitch( 's1' )
        Budapest = self.addSwitch( 's2' )
        Stuttgart = self.addSwitch( 's3' )
        Madrid = self.addSwitch( 's4' )
        Lisbon = self.addSwitch( 's5' )
        Milan = self.addSwitch( 's6' )
        Barcelona = self.addSwitch( 's7' )
        Paris = self.addSwitch( 's8' )
        London = self.addSwitch( 's9' )
        Tokyo = self.addSwitch( 's10' )
        Chicago = self.addSwitch( 's11' )
        Washington = self.addSwitch( 's12' )
        Miami = self.addSwitch( 's13' )
        LosAngeles = self.addSwitch( 's14' )
        PaloAlto = self.addSwitch( 's15' )
        SanJose = self.addSwitch( 's16' )
        HongKong = self.addSwitch( 's17' )
        Singapore = self.addSwitch( 's18' )
        Toronto = self.addSwitch( 's19' )
        NewYork = self.addSwitch( 's20' )
        Frankfurt = self.addSwitch( 's21' )
        Cologne = self.addSwitch( 's22' )
        Hanover = self.addSwitch( 's23' )
        Amsterdam = self.addSwitch( 's24' )
        Ashburn = self.addSwitch( 's25' )
        Hamburg = self.addSwitch( 's26' )
        Dortmund = self.addSwitch( 's27' )
        Dusseldorf = self.addSwitch( 's28' )
        Vienna = self.addSwitch( 's29' )
        Munich = self.addSwitch( 's30' )
        Copenhagen = self.addSwitch( 's31' )
        Stockholm = self.addSwitch( 's32' )
        Warsaw = self.addSwitch( 's33' )
        Moscow = self.addSwitch( 's34' )
        Berlin = self.addSwitch( 's35' )
        Leipzig = self.addSwitch( 's36' )
        Prague = self.addSwitch( 's37' )
        Nuremberg = self.addSwitch( 's38' )

        # ... and now hosts
        Zurich_host = self.addHost( 'h0' )
        Geneva_host = self.addHost( 'h1' )
        Budapest_host = self.addHost( 'h2' )
        Stuttgart_host = self.addHost( 'h3' )
        Madrid_host = self.addHost( 'h4' )
        Lisbon_host = self.addHost( 'h5' )
        Milan_host = self.addHost( 'h6' )
        Barcelona_host = self.addHost( 'h7' )
        Paris_host = self.addHost( 'h8' )
        London_host = self.addHost( 'h9' )
        Tokyo_host = self.addHost( 'h10' )
        Chicago_host = self.addHost( 'h11' )
        Washington_host = self.addHost( 'h12' )
        Miami_host = self.addHost( 'h13' )
        LosAngeles_host = self.addHost( 'h14' )
        PaloAlto_host = self.addHost( 'h15' )
        SanJose_host = self.addHost( 'h16' )
        HongKong_host = self.addHost( 'h17' )
        Singapore_host = self.addHost( 'h18' )
        Toronto_host = self.addHost( 'h19' )
        NewYork_host = self.addHost( 'h20' )
        Frankfurt_host = self.addHost( 'h21' )
        Cologne_host = self.addHost( 'h22' )
        Hanover_host = self.addHost( 'h23' )
        Amsterdam_host = self.addHost( 'h24' )
        Ashburn_host = self.addHost( 'h25' )
        Hamburg_host = self.addHost( 'h26' )
        Dortmund_host = self.addHost( 'h27' )
        Dusseldorf_host = self.addHost( 'h28' )
        Vienna_host = self.addHost( 'h29' )
        Munich_host = self.addHost( 'h30' )
        Copenhagen_host = self.addHost( 'h31' )
        Stockholm_host = self.addHost( 'h32' )
        Warsaw_host = self.addHost( 'h33' )
        Moscow_host = self.addHost( 'h34' )
        Berlin_host = self.addHost( 'h35' )
        Leipzig_host = self.addHost( 'h36' )
        Prague_host = self.addHost( 'h37' )
        Nuremberg_host = self.addHost( 'h38' )

        # add edges between switch and corresponding host
        self.addLink( Zurich , Zurich_host )
        self.addLink( Geneva , Geneva_host )
        self.addLink( Budapest , Budapest_host )
        self.addLink( Stuttgart , Stuttgart_host )
        self.addLink( Madrid , Madrid_host )
        self.addLink( Lisbon , Lisbon_host )
        self.addLink( Milan , Milan_host )
        self.addLink( Barcelona , Barcelona_host )
        self.addLink( Paris , Paris_host )
        self.addLink( London , London_host )
        self.addLink( Tokyo , Tokyo_host )
        self.addLink( Chicago , Chicago_host )
        self.addLink( Washington , Washington_host )
        self.addLink( Miami , Miami_host )
        self.addLink( LosAngeles , LosAngeles_host )
        self.addLink( PaloAlto , PaloAlto_host )
        self.addLink( SanJose , SanJose_host )
        self.addLink( HongKong , HongKong_host )
        self.addLink( Singapore , Singapore_host )
        self.addLink( Toronto , Toronto_host )
        self.addLink( NewYork , NewYork_host )
        self.addLink( Frankfurt , Frankfurt_host )
        self.addLink( Cologne , Cologne_host )
        self.addLink( Hanover , Hanover_host )
        self.addLink( Amsterdam , Amsterdam_host )
        self.addLink( Ashburn , Ashburn_host )
        self.addLink( Hamburg , Hamburg_host )
        self.addLink( Dortmund , Dortmund_host )
        self.addLink( Dusseldorf , Dusseldorf_host )
        self.addLink( Vienna , Vienna_host )
        self.addLink( Munich , Munich_host )
        self.addLink( Copenhagen , Copenhagen_host )
        self.addLink( Stockholm , Stockholm_host )
        self.addLink( Warsaw , Warsaw_host )
        self.addLink( Moscow , Moscow_host )
        self.addLink( Berlin , Berlin_host )
        self.addLink( Leipzig , Leipzig_host )
        self.addLink( Prague , Prague_host )
        self.addLink( Nuremberg , Nuremberg_host )

        # add edges between switches
        self.addLink( Zurich , Paris, bw=10, delay='0.839825220674ms')
        self.addLink( Zurich , Geneva, bw=10, delay='1.2697567762ms')
        self.addLink( Zurich , Stuttgart, bw=10, delay='0.790691407811ms')
        self.addLink( Zurich , Milan, bw=10, delay='1.06485775926ms')
        self.addLink( Zurich , Barcelona, bw=10, delay='0.181346667045ms')
        self.addLink( Geneva , Paris, bw=10, delay='1.33441790646ms')
        self.addLink( Geneva , Milan, bw=10, delay='0.316884634459ms')
        self.addLink( Budapest , Vienna, bw=10, delay='0.923768493648ms')
        self.addLink( Budapest , Munich, bw=10, delay='0.593619203552ms')
        self.addLink( Madrid , Paris, bw=10, delay='1.21440856492ms')
        self.addLink( Madrid , Lisbon, bw=10, delay='0.867823186843ms')
        self.addLink( Madrid , Barcelona, bw=10, delay='0.594816201724ms')
        self.addLink( Milan , Paris, bw=10, delay='1.64033197868ms')
        self.addLink( Paris , London, bw=10, delay='1.64821293722ms')
        self.addLink( Paris , Frankfurt, bw=10, delay='0.71395695023ms')
        self.addLink( Paris , Amsterdam, bw=10, delay='1.39432560693ms')
        self.addLink( Paris , Ashburn, bw=10, delay='1.64090948665ms')
        self.addLink( London , NewYork, bw=10, delay='0.829575726702ms')
        self.addLink( London , Frankfurt, bw=10, delay='1.12031625345ms')
        self.addLink( London , Amsterdam, bw=10, delay='0.396342917022ms')
        self.addLink( London , Ashburn, bw=10, delay='0.261239500883ms')
        self.addLink( London , Dusseldorf, bw=10, delay='0.220625527889ms')
        self.addLink( Tokyo , SanJose, bw=10, delay='0.846400892356ms')
        self.addLink( Tokyo , HongKong, bw=10, delay='0.447056999207ms')
        self.addLink( Chicago , Toronto, bw=10, delay='0.639397946288ms')
        self.addLink( Chicago , NewYork, bw=10, delay='0.806374975652ms')
        self.addLink( Chicago , PaloAlto, bw=10, delay='0.425874473678ms')
        self.addLink( Washington , Ashburn, bw=10, delay='0.111012024467ms')
        self.addLink( Washington , NewYork, bw=10, delay='0.605826192092ms')
        self.addLink( Washington , Miami, bw=10, delay='0.736871890949ms')
        self.addLink( Washington , LosAngeles, bw=10, delay='0.408818164439ms')
        self.addLink( LosAngeles , SanJose, bw=10, delay='1.57932360839ms')
        self.addLink( LosAngeles , HongKong, bw=10, delay='0.453793049162ms')
        self.addLink( LosAngeles , Singapore, bw=10, delay='0.520858825913ms')
        self.addLink( LosAngeles , PaloAlto, bw=10, delay='0.597240049312ms')
        self.addLink( PaloAlto , SanJose, bw=10, delay='1.29985284907ms')
        self.addLink( PaloAlto , Ashburn, bw=10, delay='0.931940619212ms')
        self.addLink( PaloAlto , NewYork, bw=10, delay='0.607535300867ms')
        self.addLink( SanJose , NewYork, bw=10, delay='1.36668930129ms')
        self.addLink( HongKong , Singapore, bw=10, delay='0.949993260681ms')
        self.addLink( Singapore , Frankfurt, bw=10, delay='0.87405058533ms')
        self.addLink( Toronto , NewYork, bw=10, delay='1.28552983241ms')
        self.addLink( NewYork , Leipzig, bw=10, delay='0.820394311868ms')
        self.addLink( NewYork , Frankfurt, bw=10, delay='1.21145333611ms')
        self.addLink( NewYork , Hanover, bw=10, delay='0.960059818424ms')
        self.addLink( NewYork , Dusseldorf, bw=10, delay='1.03206557848ms')
        self.addLink( Frankfurt , Moscow, bw=10, delay='1.14581614036ms')
        self.addLink( Frankfurt , Amsterdam, bw=10, delay='0.730024007865ms')
        self.addLink( Frankfurt , Ashburn, bw=10, delay='0.99766964831ms')
        self.addLink( Hanover , Ashburn, bw=10, delay='0.404362226448ms')
        self.addLink( Amsterdam , Hamburg, bw=10, delay='0.845692647836ms')
        self.addLink( Amsterdam , Dusseldorf, bw=10, delay='0.369792559392ms')
        self.addLink( Ashburn , Leipzig, bw=10, delay='0.341546381536ms')
        self.addLink( Ashburn , Dusseldorf, bw=10, delay='0.459956159608ms')
        self.addLink( Hamburg , Stockholm, bw=10, delay='1.02688590665ms')
        self.addLink( Hamburg , Copenhagen, bw=10, delay='0.493232754152ms')
        self.addLink( Vienna , Prague, bw=10, delay='0.69944654101ms')
        self.addLink( Vienna , Munich, bw=10, delay='0.389993816737ms')
        self.addLink( Copenhagen , Stockholm, bw=10, delay='1.32151737845ms')
        self.addLink( Warsaw , Berlin, bw=10, delay='0.387172200321ms')
        self.addLink( Warsaw , Nuremberg, bw=10, delay='1.14890042605ms')
        self.addLink( Prague , Nuremberg, bw=10, delay='1.20291601957ms')

topos = { 'generated': ( lambda: GeneratedTopo() ) }
# HERE THE CODE DEFINITION OF THE TOPOLOGY ENDS
# the following code produces an executable script working with a remote controller
# and providing ssh access to the the mininet hosts from within the ubuntu vm
controller_ip = ''

def setupNetwork(controller_ip):
    "Create network and run simple performance test"
    # check if remote controller's ip was set
    # else set it to localhost
    topo = GeneratedTopo()
    if controller_ip == '':
        #controller_ip = '10.0.2.2';
        controller_ip = '127.0.0.1';
    net = Mininet(topo=topo, controller=lambda a: RemoteController( a, ip=controller_ip, port=6633 ), host=CPULimitedHost, link=TCLink)
    return net
def connectToRootNS( network, switch, ip, prefixLen, routes ):
    "Connect hosts to root namespace via switch. Starts network."
    "network: Mininet() network object"
    "switch: switch to connect to root namespace"
    "ip: IP address for root namespace node"
    "prefixLen: IP address prefix length (e.g. 8, 16, 24)"
    "routes: host networks to route to"
    # Create a node in root namespace and link to switch 0
    root = Node( 'root', inNamespace=False )
    intf = TCLink( root, switch ).intf1
    root.setIP( ip, prefixLen, intf )
    # Start network that now includes link to root namespace
    network.start()
    # Add routes from root ns to hosts
    for route in routes:
        root.cmd( 'route add -net ' + route + ' dev ' + str( intf ) )
def sshd( network, cmd='/usr/sbin/sshd', opts='-D' ):
    "Start a network, connect it to root ns, and run sshd on all hosts."
    switch = network.switches[ 0 ]  # switch to use
    ip = '10.123.123.1'  # our IP address on host network
    routes = [ '10.0.0.0/8' ]  # host networks to route to
    connectToRootNS( network, switch, ip, 8, routes )
    for host in network.hosts:
        host.cmd( cmd + ' ' + opts + '&' )
    # DEBUGGING INFO
    print
    print "Dumping host connections"
    dumpNodeConnections(network.hosts)
    print
    print "*** Hosts are running sshd at the following addresses:"
    print
    for host in network.hosts:
        print host.name, host.IP()
    print
    print "*** Type 'exit' or control-D to shut down network"
    print
    print "*** For testing network connectivity among the hosts, wait a bit for the controller to create all the routes, then do 'pingall' on the mininet console."
    print
    CLI( network )
    for host in network.hosts:
        host.cmd( 'kill %' + cmd )
    network.stop()
if __name__ == '__main__':
    setLogLevel('info')
    #setLogLevel('debug')
    sshd( setupNetwork(controller_ip) )

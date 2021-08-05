from graphene import *
import graphene
import paramiko
import json

class Device(ObjectType):
    id = String()
    available = String()
    localstatus = String()
    role = String()
    type = String()
    mfr = String()
    hw = String()
    sw = String()
    serial = String()
    chassis = String()
    driver = String()
    channelId = String()
    managementAddress = String()
    protocol = String()

class Link(ObjectType):
    src = String()
    dst = String()
    type = String()
    state = String()

class Host(ObjectType):
    id = String()
    mac = String()
    locations = String()
    auxLocations = String()
    vlan = String()
    ips = String()
    innerVlan = String()
    outerTPID = String()
    provider = String()
    configured = String()

class IntentType(InputObjectType):
    intentOrig = String()
    macOrig = String()
    intentDest = String()
    macDest = String()

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("192.168.56.101", username="onos", password="rocks", port=8101)



class Query(ObjectType):
    # this defines a Field `hello` in our Schema with a single Argument `name`
    devices = List(Device)
    hosts = List(Host)
    liens = List(Link)
    removeIntent = String()

    # our Resolver method takes the GraphQL context (root, info) as well as
    # Argument (name) for the Field and returns data for the query Response
    def resolve_devices(root, info):
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("devices -j")
        while (ssh_stdout.channel.recv_exit_status() != 0):
            pass
        return json.load(ssh_stdout)
    
    def resolve_hosts(root, info):
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("hosts -j")
        while (ssh_stdout.channel.recv_exit_status() != 0):
            pass
        return json.load(ssh_stdout)
    
    def resolve_liens(root, info):
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("links -j")
        while (ssh_stdout.channel.recv_exit_status() != 0):
            pass
        return json.load(ssh_stdout)

    def resolve_removeIntent(root, info):
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("remove-intent -p")
        while (ssh_stdout.channel.recv_exit_status() != 0):
            pass
        return "Suppression des intents OK"

class AddIntent(Mutation):
    class Arguments:
        intentList = graphene.List(IntentType)
    
    ok = Boolean()

    def mutate(cls, root, intentList):
        
        for elt in intentList:
            print(elt)
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("add-point-intent "+" -s "+elt["macOrig"]+" -d "+elt["macDest"]+" -t IPV4 "+elt["intentOrig"]+" "+elt["intentDest"])
            while (ssh_stdout.channel.recv_exit_status() != 0):
                pass
        return AddIntent(ok="ok")


class Mutation(ObjectType):
    addIntent = AddIntent.Field()

schema = Schema(
    query=Query,
    mutation=Mutation
)


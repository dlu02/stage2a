from websocket_server import WebsocketServer
import paramiko


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("192.168.56.101", username="onos", password="rocks", port=8101)


# Called for every client connecting (after handshake)
def new_client(client, server):
    global devices_orig,hosts_orig,links_orig
    print("New client connected and was given id %d" % client['id'])
    ssh_stdin1, ssh_stdout1, ssh_stderr1 = ssh.exec_command("devices -j")
    while (ssh_stdout1.channel.recv_exit_status() != 0):
        pass
    devices_orig = ssh_stdout1.read().decode('ascii').strip()

    ssh_stdin2, ssh_stdout2, ssh_stderr2 = ssh.exec_command("hosts -j")
    while (ssh_stdout2.channel.recv_exit_status() != 0):
        pass
    hosts_orig = ssh_stdout2.read().decode('ascii').strip()

    ssh_stdin3, ssh_stdout3, ssh_stderr3 = ssh.exec_command("links -j")
    while (ssh_stdout3.channel.recv_exit_status() != 0):
        pass
    links_orig = ssh_stdout3.read().decode('ascii').strip()
    server.send_message_to_all("Hey all, a new client has joined us")


# Called for every client disconnecting
def client_left(client, server):
	print("Client(%d) disconnected" % client['id'])


# Called when a client sends a message
def message_received(client, server, message):
    print("Client(%d) said: %s" % (client['id'], message))
    if message == "dev":
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("devices -j")
        while (ssh_stdout.channel.recv_exit_status() != 0):
            pass
        res_potentiel = ssh_stdout.read().decode('ascii').strip()
        if res_potentiel != devices_orig:
            devices_orig = res_potentiel
            server.send_message(client, res_potentiel)
        else:
            server.send_message(client, "OK devices")
    if message == "hosts":
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("hosts -j")
        while (ssh_stdout.channel.recv_exit_status() != 0):
            pass
        res_potentiel = ssh_stdout.read().decode('ascii').strip()
        if res_potentiel != hosts_orig:
            hosts_orig = res_potentiel
            server.send_message(client, res_potentiel)
        else:
            server.send_message(client, "OK hosts")

    if message == "links":
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("links -j")
        while (ssh_stdout.channel.recv_exit_status() != 0):
            pass
        res_potentiel = ssh_stdout.read().decode('ascii').strip()
        if res_potentiel != links_orig:
            links_orig = res_potentiel
            server.send_message(client, res_potentiel)
        else:
            server.send_message(client, "OK links")


PORT=8000
server = WebsocketServer(PORT)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()
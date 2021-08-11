import asyncio
import websockets
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("192.168.56.101", username="onos", password="rocks", port=8101)


ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("devices -j")
while (ssh_stdout.channel.recv_exit_status() != 0):
    pass
devices_orig = ssh_stdout.read().decode('ascii').strip()

ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("hosts -j")
while (ssh_stdout.channel.recv_exit_status() != 0):
    pass
hosts_orig = ssh_stdout.read().decode('ascii').strip()

ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("links -j")
while (ssh_stdout.channel.recv_exit_status() != 0):
    pass
links_orig = ssh_stdout.read().decode('ascii').strip()
    

# create handler for each connection
async def handler(websocket, path):
    res = []
    data = await websocket.recv()
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("devices -j")
    while (ssh_stdout.channel.recv_exit_status() != 0):
        pass
    res_potentiel = ssh_stdout.read().decode('ascii').strip()
    if res_potentiel != devices_orig:
        res.append(res_potentiel)
        devices_orig = res_potentiel
    else:
        res.append("OK devices")

    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("hosts -j")
    while (ssh_stdout.channel.recv_exit_status() != 0):
        pass
    res_potentiel = ssh_stdout.read().decode('ascii').strip()
    if res_potentiel != hosts_orig:
        res.append(res_potentiel)
        hosts_orig = res_potentiel
    else:
        res.append("OK hosts")

    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("links -j")
    while (ssh_stdout.channel.recv_exit_status() != 0):
        pass
    res_potentiel = ssh_stdout.read().decode('ascii').strip()
    if res_potentiel != hosts_orig:
        res.append(res_potentiel)
        hosts_orig = res_potentiel
    else:
        res.append("OK devices")

    await websocket.send(', '.join(res))
    

start_server = websockets.serve(handler, "127.0.0.1", 8000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
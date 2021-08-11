import flask
from flask import Flask
import paramiko
import json

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("192.168.56.101", username="onos", password="rocks", port=8101)

app = Flask(__name__)
app.debug = True

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

def detect_chgt_device(devices_or):
    ssh_stdin1, ssh_stdout1, ssh_stderr1 = ssh.exec_command("devices -j")
    while (ssh_stdout1.channel.recv_exit_status() != 0):
        pass
    potentiel = ssh_stdout1.read().decode('ascii').strip()
    new_pot = json.loads(potentiel)
    json_pot = json.loads(devices_or)
    for elt in new_pot:
        del elt['humanReadableLastUpdate']
    for elt in json_pot:
        del elt['humanReadableLastUpdate']
    if new_pot != json_pot:
        return potentiel
    else:
        return "ok"

def detect_chgt_host(devices_ho):
    ssh_stdin1, ssh_stdout1, ssh_stderr1 = ssh.exec_command("hosts -j")
    while (ssh_stdout1.channel.recv_exit_status() != 0):
        pass
    potentiel = ssh_stdout1.read().decode('ascii').strip()
    if potentiel != devices_ho:
        return potentiel
    else:
        return "ok"

def detect_chgt_links(devices_link):
    ssh_stdin1, ssh_stdout1, ssh_stderr1 = ssh.exec_command("links -j")
    while (ssh_stdout1.channel.recv_exit_status() != 0):
        pass
    potentiel = ssh_stdout1.read().decode('ascii').strip()
    if potentiel != devices_link:
        return potentiel    
    else:
        return "ok"

@app.route('/changes/devices', methods=['GET'])
def getChangesDevices():
    global devices_orig
    print(devices_orig)
    pot = detect_chgt_device(devices_orig)
    print("\n new \n")
    print(pot)
    if pot == "ok":
        flask.abort(404, description="Identiques")
    else:
        devices_orig = pot
        return flask.jsonify(json.loads(pot))

@app.route('/changes/hosts', methods=['GET'])
def getChangesHosts():
    global hosts_orig
    pot = detect_chgt_host(hosts_orig)
    if pot == "ok":
        flask.abort(404)
    else:
        hosts_orig = pot
        return flask.jsonify(json.loads(pot))


@app.route('/changes/links', methods=['GET'])
def getChangesLinks():
    global links_orig
    pot = detect_chgt_links(links_orig)
    if pot == "ok":
        flask.abort(404)
    else:
        links_orig = pot
        return flask.jsonify(json.loads(pot))


if __name__ == '__main__':
    app.run(host="127.0.0.1",port=8081,debug=True)
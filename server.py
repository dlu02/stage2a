from flask import Flask
from flask_graphql import GraphQLView
from schema import schema
import flask
import paramiko
import json

app = Flask(__name__)
app.debug = True


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("192.168.1.154", username="onos", password="rocks", port=8101)


@app.route('/rest/devices', methods=['GET'])
def getDevices():
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("devices -j")
    return flask.jsonify(json.loads(ssh_stdout.read().decode('ascii').strip()))

@app.route('/rest/hosts', methods=['GET'])
def getHosts():
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("hosts -j")
    return flask.jsonify(json.loads(ssh_stdout.read().decode('ascii').strip()))

@app.route('/rest/links', methods=['GET'])
def getLinks():
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("links -j")
    return flask.jsonify(json.loads(ssh_stdout.read().decode('ascii').strip()))

@app.route('/rest/intent', methods=['GET'])
def installIntent():
    orig = flask.request.args.get('orig')
    dest = flask.request.args.get('dest')
    mac_orig = flask.request.args.get('macorig')
    mac_dest = flask.request.args.get('macdest')
    orig = orig.replace("-","/")
    dest = dest.replace("-","/")
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("add-point-intent "+" -s "+mac_orig+" -d "+mac_dest+" -t IPV4 "+orig+" "+dest)
    return flask.jsonify({"data": {"addIntent": {"ok": True }}})

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

if __name__ == '__main__':
    app.run()
from flask import Flask
from flask_graphql import GraphQLView
from schema import schema
import flask
import paramiko
import json
import subprocess

app = Flask(__name__)
app.debug = True


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("192.168.56.101", username="onos", password="rocks", port=8101)


@app.route('/rest/devices', methods=['GET'])
def getDevices():
    sub = subprocess.Popen("onos localhost devices -j", shell=True, stdout=subprocess.PIPE)
    subprocess_return = sub.stdout.read()
    return flask.jsonify(json.loads(subprocess_return.decode('ascii').strip()))

@app.route('/rest/hosts', methods=['GET'])
def getHosts():
    sub = subprocess.Popen("onos localhost hosts -j", shell=True, stdout=subprocess.PIPE)
    subprocess_return = sub.stdout.read()
    return flask.jsonify(json.loads(subprocess_return.decode('ascii').strip()))

@app.route('/rest/links', methods=['GET'])
def getLinks():
    sub = subprocess.Popen("onos localhost links -j", shell=True, stdout=subprocess.PIPE)
    subprocess_return = sub.stdout.read()
    return flask.jsonify(json.loads(subprocess_return.decode('ascii').strip()))

@app.route('/rest/intent', methods=['GET'])
def installIntent():
    orig = flask.request.args.get('orig')
    dest = flask.request.args.get('dest')
    mac_orig = flask.request.args.get('macorig')
    mac_dest = flask.request.args.get('macdest')
    orig = orig.replace("-","/")
    dest = dest.replace("-","/")
    sub = subprocess.Popen("onos localhost add-point-intent "+" -s "+mac_orig+" -d "+mac_dest+" -t IPV4 "+orig+" "+dest, shell=True, stdout=subprocess.PIPE)
    subprocess_return = sub.stdout.read()
    return flask.jsonify({"data": {"addIntent": {"ok": True }}})

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

if __name__ == '__main__':
    app.run()
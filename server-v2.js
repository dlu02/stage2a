const express = require('express')
const expressGraphQL = require('express-graphql').graphqlHTTP
const system = require('system-commands')
const fs = require('fs')

var child_process = require('child_process');

const {
    GraphQLSchema, 
    GraphQLObjectType,
    GraphQLString,
    GraphQLList,
    GraphQLInt,
    GraphQLNonNull,
    GraphQLScalarType,
    GraphQLBoolean,
    GraphQLInputObjectType,
    GraphQLOutputObjectType
} = require('graphql')

const { GraphQLJSON } = require('graphql-type-json');

const app = express()

const path = require('path');
const {NodeSSH} = require('node-ssh');

const ssh = new NodeSSH();

var va;

// exécution de la fonction f (issue de l'api rest d'onos) + parsage de la réponse
function doFunction(f) {
    const str = 'onos localhost '
    const newstr = str+f+" -j";
    const str1 = child_process.execSync(newstr);
    return str1
}

function doAddIntentExt(elt_intent_liste) {
    const cmd = "onos localhost add-point-intent -s "+elt_intent_liste["mac_orig"]+" -d "+elt_intent_liste["mac_dest"]+" -t IPV4 "+elt_intent_liste["intent_orig"]+" "+elt_intent_liste["intent_dest"]
    const str1 = child_process.execSync(cmd)
    console.log(cmd)
    return "OK" 
}

ssh.connect({
    host: '192.168.1.154',
    port: 8101,
    username: 'onos',
    password: 'rocks'
  }).then(function() {

        // type device pour un appareil du cluster
        const DeviceType = new GraphQLObjectType({
            name: 'Device',
            description: 'Appareil du cluster ONOS',
            fields: () => ({
                id: { type: GraphQLNonNull(GraphQLString) },
                available: { type: GraphQLNonNull(GraphQLString)},
                localstatus: { type: GraphQLNonNull(GraphQLString)},
                // author: {
                //     type: AuthorType,
                //     resolve: (books) => {
                //         return authors.find(author => author.id === books.authorId)
                //     }
                // }
                role: { type: GraphQLNonNull(GraphQLString)},
                type: { type: GraphQLNonNull(GraphQLString)},
                mfr: { type: GraphQLNonNull(GraphQLString)},
                hw: { type: GraphQLNonNull(GraphQLString)},
                sw: { type: GraphQLNonNull(GraphQLString)},
                serial: { type: GraphQLNonNull(GraphQLString)},
                chassis: { type: GraphQLNonNull(GraphQLInt)},
                driver: { type: GraphQLNonNull(GraphQLString)},
                channelId: { type: GraphQLNonNull(GraphQLString)},
                managementAddress: { type: GraphQLNonNull(GraphQLString)},
                protocol: { type: GraphQLNonNull(GraphQLString)},
            })
        })

        // type lien pour un lien du cluster
        const LinkType = new GraphQLObjectType({
            name: 'Liens',
            description: 'Un lien du cluster ONOS',
            fields: () => ({
                src: { type: GraphQLJSON},
                dst: { type: GraphQLJSON},
                type: { type: GraphQLNonNull(GraphQLString)},
                state: { type: GraphQLNonNull(GraphQLString)}
            })
        })

        // type hosts pour un host du cluster
        const HostType = new GraphQLObjectType({
            name: 'Hosts',
            description: 'Un host du cluster ONOS',
            fields: () => ({
                id: { type: GraphQLNonNull(GraphQLString)},
                mac: { type: GraphQLNonNull(GraphQLString)},
                locations: { type: GraphQLJSON},
                auxLocations: { type: GraphQLNonNull(GraphQLString)},
                vlan: { type: GraphQLNonNull(GraphQLString)},
                ips: { type: GraphQLNonNull(GraphQLString)},
                innerVlan: { type: GraphQLNonNull(GraphQLString)},
                outerTPID: { type: GraphQLNonNull(GraphQLString)},
                provider: { type: GraphQLNonNull(GraphQLString)},
                configured: { type: GraphQLNonNull(GraphQLString)}
            })
        })
        // implémentation des requêtes graphql
        const RootQueryType = new GraphQLObjectType({
            name: 'Query',
            description: 'Root Query',
            fields: () => ({
                devices: {
                    type: new GraphQLList(DeviceType),
                    description: 'List of all devices',
                    resolve: () => JSON.parse(doFunction('devices'))
                },
                device: {
                    type: DeviceType,
                    description: 'A Single Device',
                    args: {
                        id: { type: GraphQLString }
                    },
                    resolve: (parent, args) => JSON.parse(doFunction('devices')).find(device => device.id === args.id)
                },
                liens: {
                    type: new GraphQLList(LinkType),
                    description: 'List of all links',
                    resolve: () => JSON.parse(doFunction('links'))
                },
                hosts: {
                    type: new GraphQLList(HostType),
                    description: 'List of all hosts',
                    resolve: () => JSON.parse(doFunction('hosts'))
                }
            })
        })


        const IntentType = new GraphQLObjectType({
            name: 'Intent',
            description: 'Un intent entre deux ports',
            fields: () => ({
                intent_orig: { type: GraphQLNonNull(GraphQLString) },
                mac_orig: { type: GraphQLNonNull(GraphQLString) },
                intent_dest:  { type: GraphQLNonNull(GraphQLString) },
                mac_dest: { type: GraphQLNonNull(GraphQLString) }
            })
        })

        const IntentListInput = new GraphQLInputObjectType({
            name: 'IntentListInput',
            fields: {
                intent_orig: { type: GraphQLNonNull(GraphQLString) },
                mac_orig: { type: GraphQLNonNull(GraphQLString) },
                intent_dest:  { type: GraphQLNonNull(GraphQLString) },
                mac_dest: { type: GraphQLNonNull(GraphQLString) }
            }
        });

        const RootMutationType = new GraphQLObjectType({
            name: 'Mutation',
            description: 'Root Mutation',
            fields: () => ({
                addIntent: {
                    type: IntentType,
                    description: 'Ajouter un intent',
                    args: {
                        intent_orig: { type: GraphQLNonNull(GraphQLString) },
                        mac_orig: { type: GraphQLNonNull(GraphQLString) },
                        intent_dest:  { type: GraphQLNonNull(GraphQLString) },
                        mac_dest: { type: GraphQLNonNull(GraphQLString) }
                    },
                    resolve: (parent, args) => {
                        return ssh.execCommand("add-point-intent "+" -s "+args.mac_orig+" -d "+args.mac_dest+" -t IPV4 "+args.intent_orig+" "+args.intent_dest).then((result) => console.log(result.stdout)).then(() => JSON.parse('{ "intent_orig": "'+args.intent_orig+'", "mac_orig": "'+args.mac_orig+'", "intent_dest": "'+args.intent_dest+'", "mac_dest": "'+args.mac_dest+'" }'))
                    }
                },
                addIntent3: {
                    type: GraphQLList(IntentType),
                    description: 'Ajouter une liste de intents',
                    args: {
                        input: { type: GraphQLList(IntentListInput) },
                    },
                    resolve: (parent, args) => { 
                        for (elt in args.input) {
                            doAddIntentExt(elt)
                            console.log("OK Ajout Intent")
                        }
                        
                        
                    }
                },
                addIntent2: {
                    type: GraphQLList(IntentType),
                    description: 'Ajouter une liste de intents',
                    args: {
                        input: { type: GraphQLList(IntentListInput) },
                    },
                    resolve: (parent, args) => { 
                        async function parcoursListe(liste, i) {
                            if (i >= liste.length) {
                                console.log("ok")
                            }
                            else {
                                const temp = await ssh.execCommand("add-point-intent "+" -s "+liste[i]["mac_orig"]+" -d "+liste[i]["mac_dest"]+" -t IPV4 "+liste[i]["intent_orig"]+" "+liste[i]["intent_dest"]).then((result) => console.log(result.stdout)).then(() => parcoursListe(liste, i+1))
                            }
                        }


                        // async function doBoucle() {
                        //     for (i = 0 ; i < (args.input.length) ; i++) {
                        //         await parcoursListe(args.input[i])
                        //     }
                        // }
                        async function doF() {
                            return await parcoursListe(args.input, 0)
                        }

                        doF()
                        
                    }
                },
                removeIntent: {
                    type: GraphQLString,
                    resolve: (parent, args) => {
                        return ssh.execCommand("remove-intent -p").then((result) => console.log(result.stdout))
                    }
                }
            })
        })

        // construction du schéma graphql
        const schema = new GraphQLSchema({
            query: RootQueryType,
            mutation: RootMutationType
        })

        // construction du serveur graphql
        app.use('/graphql', expressGraphQL({
            schema: schema,
            graphiql: true,
        }))

        // api rest
        app.get('/devices', (req,res) => {
            ssh.execCommand("devices -j").then((result) => { res.status(200).json(JSON.parse(result.stdout))  })
        })

        app.get('/links', (req,res) => {
            ssh.execCommand("links -j").then((result) => { res.status(200).json(JSON.parse(result.stdout))  })
        })

        app.get('/hosts', (req,res) => {
            ssh.execCommand("hosts -j").then((result) => { res.status(200).json(JSON.parse(result.stdout))  })
        })

        app.get('/removeIntents', (req,res) => {
            res.setHeader('Content-Type', 'application/json');
            ssh.execCommand("remove-intent -p")
            res.status(200).json(JSON.stringify("ok"))
        })

        app.get('/intent', (req,res) => {
            const orig = req.query.orig.replaceAll("-","/");
            const dest = req.query.dest.replaceAll("-","/");
            const macorig = req.query.macorig;
            const macdest = req.query.macdest;
            ssh.execCommand("add-point-intent "+" -s "+macorig+" -d "+macdest+" -t IPV4 "+orig+" "+dest).then((result) => { res.status(200).json(JSON.stringify("ok")) }) 
            
        })
  })


app.listen(5000., () => console.log('Server Running'))
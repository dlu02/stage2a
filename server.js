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
    GraphQLBoolean
} = require('graphql')

const { GraphQLJSON } = require('graphql-type-json');

const app = express()

// exécution de la fonction f (issue de l'api rest d'onos) + parsage de la réponse
function doFunction(f) {
    const str = 'onos localhost '
    const newstr = str+f+" -j";
    const str1 = child_process.execSync(newstr);
    return str1
}
// fs.writeFile('test7.json', doFunction('devices'), () => {})
// const test = JSON.parse(doFunction('hosts'))
// // test["locations"] = JSON.parse(test["locations"])
// // for (var elt in test) {
// //     const temp = (elt["locations"])[0]
// //     elt.locations = JSON.stringify(temp)
// // }
// for (const elt of test) {
//     const temp = elt["locations"]
//     elt["locations"] = JSON.stringify(temp)
// }
// // console.log(test[2].locations[0])
// console.log(test)

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

// const RootMutationType = new GraphQLObjectType({
//     name: 'Mutation',
//     description: 'Root Mutation',
//     fields: () => ({
//         addBook: {
//             type: BookType,
//             description: 'Add a book',
//             args: {
//                 name: { type: GraphQLNonNull(GraphQLString) },
//                 authorId: {type: GraphQLNonNull(GraphQLInt)}
//             },
//             resolve: (parent, args) => {
//                 const book = { id: books.length +1, name: args.name, authorId: args.authorId }
//                 books.push(book)
//                 return book
//             }
//         },
//         addAuthor: {
//             type: AuthorType,
//             description: 'Add an author',
//             args: {
//                 name: { type: GraphQLNonNull(GraphQLString) },
//             },
//             resolve: (parent, args) => {
//                 const author = { id: authors.length +1, name: args.name }
//                 authors.push(author)
//                 return author
//             }
//         }
//     })
// })

// construction du schéma graphql
const schema = new GraphQLSchema({
    query: RootQueryType,
    // mutation: RootMutationType
})

// construction du serveur graphql
app.use('/graphql', expressGraphQL({
    schema: schema,
    graphiql: true,
}))

// api rest
app.get('/devices', (req,res) => {
    res.status(200).json(JSON.parse(doFunction('devices')))
})

app.get('/links', (req,res) => {
    res.status(200).json(JSON.parse(doFunction('links')))
})

app.get('/hosts', (req,res) => {
    res.status(200).json(JSON.parse(doFunction('hosts')))
})

app.listen(5000., () => console.log('Server Running'))
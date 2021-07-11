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
const app = express()

// exécution de la fonction f (issue de l'api rest d'onos) + parsage de la réponse
function doFunction(f) {
    const str = 'cd /home/damien && ./onos/tools/test/bin/onos localhost '
    const newstr = str.concat(f);
    const str1 = child_process.execSync(newstr).toString();
    const strb = str1.replaceAll("Nicira, Inc.","Nicira Inc.")
    const str2 = strb.replaceAll('=','":"')
    const str3 = str2.replaceAll(', ','","')
    const str4 = str3.replaceAll('\n','"},\n')
    const str5 = str4.replaceAll("provider","pvers")
    const str5b = str5.replaceAll('local-status','localstatus')
    const str6a = str5b.replaceAll('src','{"src')
    const str6b = str6a.replaceAll("ip(s)","ips")
    const str7 = str6b.replaceAll("id",'{"id')
    const str6 = '['+str7+']2'
    return str6.replace(',\n]2',']')
}
// fs.writeFile('test7.json', doFunction('devices'), () => {}) 
// console.log(JSON.parse(doFunction('hosts')))


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
        src: { type: GraphQLNonNull(GraphQLString)},
        dst: { type: GraphQLNonNull(GraphQLString)},
        type: { type: GraphQLNonNull(GraphQLString)},
        state: { type: GraphQLNonNull(GraphQLString)},
        expected: { type: GraphQLNonNull(GraphQLString)}
    })
})

// type hosts pour un host du cluster
const HostType = new GraphQLObjectType({
    name: 'Hosts',
    description: 'Un host du cluster ONOS',
    fields: () => ({
        id: { type: GraphQLNonNull(GraphQLString)},
        mac: { type: GraphQLNonNull(GraphQLString)},
        locations: { type: GraphQLNonNull(GraphQLString)},
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
app.listen(5000., () => console.log('Server Running'))
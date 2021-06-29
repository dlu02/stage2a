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

function doFunction(f) {
    const str = 'cd /home/damien && ./onos/tools/test/bin/onos localhost '
    const newstr = str.concat(f);
    const str1 = child_process.execSync(newstr).toString();
    const strb = str1.replaceAll("Nicira, Inc.","Nicira Inc.")
    const str2 = strb.replaceAll('=','":"')
    const str3 = str2.replaceAll(', ','","')
    const str4 = str3.replaceAll('\n','"},\n')
    const str5 = str4.replaceAll('id','{"id')
    const str5b = str5.replaceAll('local-status','localstatus')
    const str6 = '['+str5b+']2'
    return str6.replace(',\n]2',']')
}
// fs.writeFile('test7.json', doFunction('devices'), () => {}) 
console.log(JSON.parse(doFunction('devices')))

// const authors = [
// 	{ id: 1, name: 'J. K. Rowling' },
// 	{ id: 2, name: 'J. R. R. Tolkien' },
// 	{ id: 3, name: 'Brent Weeks' }
// ]

// const books = [
// 	{ id: 1, name: 'Harry Potter and the Chamber of Secrets', authorId: 1 },
// 	{ id: 2, name: 'Harry Potter and the Prisoner of Azkaban', authorId: 1 },
// 	{ id: 3, name: 'Harry Potter and the Goblet of Fire', authorId: 1 },
// 	{ id: 4, name: 'The Fellowship of the Ring', authorId: 2 },
// 	{ id: 5, name: 'The Two Towers', authorId: 2 },
// 	{ id: 6, name: 'The Return of the King', authorId: 2 },
// 	{ id: 7, name: 'The Way of Shadows', authorId: 3 },
// 	{ id: 8, name: 'Beyond the Shadows', authorId: 3 }
// ]


/* const schema = new GraphQLSchema({
    query: new GraphQLObjectType({
        name: 'HelloWorld',
        fields: () => ({
            message: { 
                type: GraphQLString, 
                resolve: () => 'Hello World'
            }
        })
    })
}) */

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
        chassis: { type: GraphQLNonNull(GraphQLString)},
        driver: { type: GraphQLNonNull(GraphQLString)},
        channelId: { type: GraphQLNonNull(GraphQLString)},
        managementAddress: { type: GraphQLNonNull(GraphQLString)},
        protocol: { type: GraphQLNonNull(GraphQLString)},
    })
})

const RootQueryType = new GraphQLObjectType({
    name: 'Query',
    description: 'Root Query',
    fields: () => ({
        devices: {
            type: new GraphQLList(DeviceType),
            description: 'List of all devices',
            resolve: () => JSON.parse(doFunction('devices'))
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

const schema = new GraphQLSchema({
    query: RootQueryType,
    // mutation: RootMutationType
})

app.use('/graphql', expressGraphQL({
    schema: schema,
    graphiql: true
}))
app.listen(5000., () => console.log('Server Running'))
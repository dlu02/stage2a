# Code source stage 2a ENSIIE 2021

## Installation

1. Installer nodejs et npm, puis ses paquets associés :
```
$ pacman -S npm
```

2. Créer un projet dans npm :
```
$ mkdir stage2a
$ npm init
```

3. Installer les modules :
```
$ npm install express express-graphql graphql
$ npm install --save-dev nodemon
```

4. Remplacer dans `package.json` la partie scripts par :
```
  "scripts": {
    "devStart": "nodemon server.js"
  },
```

# Code source stage 2a ENSIIE 2021

Voici le code source du stage 2A 2021 : il permet de créer une application de routage dynamique ou statique à partir d'un réseau SDN et également de créer le serveur GraphQL/REST nécessaire pour traiter les requêtes.

> Le code à jour pour tout le stage se trouve UNIQUEMENT dans cette branche `new`. Les autres branches ne sont pas à jour et seront bientôt supprimées.

## Contenu

Ce dépôt contient :
- le code source des applications de routage statique et dynamique (dossiers `app-routage-statique` et `app-routage-dynamique`)
- le code source du fichier de test ayant servi à la génération des graphiques (dossier `tests-app`)
- le code source nécessaire pour la génération des topologies personnalisées (dossier `topologies-custom`)
- le code source du serveur de backend GraphQL/Rest dans les versions Python et NodeJS (dossiers `serv_graphql_vNodejs` et `serv_graphql_vPython`)

> La version NodeJS du serveur de backend est DÉPRÉCIÉE : utiliser plutôt la version Python !!

## Prérequis

Les tests et l'implémentation ont été réalisés avec une machine hébergeant à la fois le serveur de backend GraphQL/Rest et le contrôleur ONOS. Les applications de routage ainsi que les tests sont installés sur une autre machine physique de sorte à pouvoir simuler un environnement réaliste d'implémentation de réseau SDN.

Sur la machine hébergeant le contrôleur SDN, sont nécessaires :

- un contrôleur SDN bien sûr, dans notre cas, il s'agit d'ONOS qui tourne donc en localhost
- le paquet `mininet` correctement configuré
- Python 3.6+ avec les modules Flask, NetworkX, Matplotlib, Numpy et Graphene
- Python 2.7+ avec le module Mininet
- une configuration correcte du fichier `/etc/hosts` de sorte à pouvoir rediriger `127.0.0.1` vers l'IP locale de la machine

Sur la machine hébergeant les applications, est nécessaire :

- Python 3.6+ avec le module Jupyter

Une configuration plus détaillée est décrite dans chacun des dossiers.

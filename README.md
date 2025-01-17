# Puissance 4

Ce dépôt Github contient le code du projet final pour le cours de Système d'exploitation et virtualisation

Pour lancer ce projet, vous devez définir dans l'environnement :
- L'adresse IP du serveur pour le client avec IP_ADRESSE_SERVEUR
- L'adresse IP serveur peut aussi être définie avec IP_ADRESSE_SERVEUR mais ceci est <ins>optionnelle</ins> !!!

Le port par défaut pour les sessions de jeu est le port 6000 et le port de l'interface web est le 6001.

N'hésitez pas à modifier le docker compose pour l'adapter à la machine (notamment l'URL du registre contenant les
images et les variables d'environnement) !

LANCER LE SERVEUR EN PREMIER !!!

Pour lancer le serveur sur Linux 1:
```shell
docker compose -f docker-compose_serveur.yml up
```

Pour lancer le client sur Linux 2:
```shell
docker compose -f docker-compose_client.yml up
```

Pour lancer le client sur windows :
- Double clique sur <ins>start_client</ins> dans le dossier Puissance4

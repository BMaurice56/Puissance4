# Puissance 4

Ce dépôt Github contient le code du projet final pour le cours de Système d'exploitation et virtualisation

Pour lancer ce projet, vous devez définir dans l'environnement :
- L'adresse IP du serveur pour le client avec IP_ADRESSE_SERVEUR
- L'adresse IP serveur peut aussi être définie avec IP_ADRESSE_SERVEUR mais ceci est optionnelle !

Le port par défaut pour les sessions de jeu est le port 6000 et le port de l'interface web est le 6001.

N'hésitez pas à modifier le docker compose pour l'adapter à la machine (notamment l'URL du registre contenant les
images et les variables d'environnement) !

Pour lancer le serveur :
```shell
docker compose -f docker-compose_serveur.yml up
```

Pour lancer le client :
```shell
docker compose -f docker-compose_client.yml up
```

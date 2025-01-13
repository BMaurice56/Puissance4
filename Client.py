import socket
import Minimax
import pickle
import os
from copy import deepcopy
from random import randint

ip_address = os.environ["IP_ADRESSE_SERVEUR"]
port = 6000
joueur = 1


def connect_to_server(host, port_serveur):
    # Execute 5 parties
    for i in range(5):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        profondeur_reflexion_ia = randint(1, 5)

        try:
            client_socket.connect((host, port_serveur))
            print(f"Connecté au serveur {host}:{port_serveur}")

            client_socket.send(bytes(profondeur_reflexion_ia))

            while True:
                # Réception de la grille
                data = client_socket.recv(1024)
                if not data or data == b"END":
                    break

                grille = pickle.loads(data)

                # Calcul du coup
                arbre = Minimax.arbre_possibles(
                    Minimax.Arbre((deepcopy(grille), None)),
                    joueur, profondeur_reflexion_ia)
                _, coup = Minimax.minimax(arbre, True, joueur)

                # Envoi du coup
                client_socket.send(pickle.dumps(coup))

        except ConnectionRefusedError:
            print(f"Impossible de se connecter à {host}:{port_serveur}")
        except Exception as e:
            print(f"Erreur : {e}")
        finally:
            client_socket.close()
            print("Connexion fermée.")


connect_to_server(ip_address, port)

import asyncio
import pickle
import Minimax
import os
from aiohttp import web
from copy import deepcopy
from random import randint

ip_address = os.environ.get("IP_ADRESSE_SERVEUR", "0.0.0.0")
port = 6000
web_port = 6001

id_parties = []
parties = {}


def generation_id_partie() -> int:
    """
    Génère un id unique de partie
    """
    id_party = randint(0, 10_000_000)

    while id_party in id_parties:
        id_party = randint(0, 10_000_000)

    return id_party


def creation_grille() -> list:
    """
    Crée une grille de jeu
    """
    return deepcopy(Minimax.grille)


def jouer_coup(coup: str, id_partie: int, joueur: int) -> None:
    """
    Joue un coup pour un joueur donné
    """
    Minimax.joue_coup(coup, parties[id_partie]["grille"], joueur)

    parties[id_partie]["etat_jeu"] = f"Le joueur {int(joueur)} ({Minimax.jetons[joueur]}) a joué {coup}"


async def handle_http_request(_request):
    """
    Génère une page HTML avec l'état actuel de toutes les parties, y compris les niveaux des joueurs.
    Les parties sont affichées sur une ligne avec défilement latéral.
    """
    # Construction du tableau HTML des parties
    partie_html = ""
    for id_p in id_parties:
        grille_str = Minimax.affichage_str(parties[id_p]["grille"]).replace("\n", "<br>")
        etat_jeu = parties[id_p]["etat_jeu"]
        level_joueur_0 = parties[id_p]["level_joueur_0"]
        level_joueur_1 = parties[id_p]["level_joueur_1"]
        jeu_fini = parties[id_p]["jeu_fini"]

        bouton_supprimer = ""
        if jeu_fini:
            bouton_supprimer = f"""<button onclick="deletePartie({id_p})" style="margin-top: 10px;">🗑️ Supprimer</button>"""

        partie_html += f"""
        <div style="min-width: 300px; margin: 10px; padding: 10px; border: 1px solid black; flex: 0 0 auto;">
            <h3>Partie ID: {id_p}</h3>
            <p><strong>Niveau Joueur 0 ({Minimax.jetons[0]}) :</strong> {level_joueur_0}/5</p>
            <p><strong>Niveau Joueur 1 ({Minimax.jetons[1]}) :</strong> {level_joueur_1}/5</p>
            <p>Grille:</p>
            <pre>{grille_str}</pre>
            <p>État: {etat_jeu}</p>
            {bouton_supprimer}
        </div>
        """

    # Page HTML avec défilement latéral et gestion AJAX
    head = """
    <head>
        <title>État des Parties</title>
        <meta http-equiv="refresh" content="3"> <!-- Refresh toutes les 3 secondes -->
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 20px;
                background-color: #f0f0f0;
            }}
            .container {{
                display: block;
                margin: 0 auto;
            }}
            div {{
                background-color: #fff;
                border-radius: 5px;
                box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.2);
            }}
        </style>
        <script>
            async function deletePartie(id_p) {
                try {
                    const url = "/delete/" + id_p;
            
                    const response = await fetch(url, { method: 'DELETE' });
                    if (response.ok) {
                        alert("Partie supprimée !");
                        location.reload();
                    } else {
                        alert("Échec de la suppression : Partie introuvable.");
                    }
                } catch (error) {
                    console.error("Erreur lors de la suppression :", error);
                    alert("Une erreur s'est produite lors de la suppression.");
                }
            }
        </script>
    </head>
    """

    body = f"""
    <body>
        <h1>État des Parties en Cours</h1>
        <div class="container">
            {partie_html}
        </div>
    </body>
    """

    html = f"""
    <!DOCTYPE html>
    <html>
    {head}
    {body}
    </html>
    """
    return web.Response(text=html, content_type="text/html")


async def delete_partie(request):
    """
    Supprime une partie terminée selon son ID.
    """
    id_p = int(request.match_info.get('id'))
    if id_p in id_parties:
        del parties[id_p]
        id_parties.remove(id_p)
        return web.Response(text="Partie supprimée", status=200)
    else:
        return web.Response(text="Partie introuvable", status=404)


async def start_http_server():
    """
    Démarre le serveur HTTP pour pouvoir visualiser les parties en cours.
    """
    app = web.Application()
    app.router.add_get('/', handle_http_request)
    app.router.add_delete('/delete/{id}', delete_partie)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, ip_address, web_port)
    await site.start()
    print(f"Serveur HTTP en écoute sur http://{ip_address}:{web_port}")


async def handle_tcp_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    compteur = 0
    game_finished = False
    joueur = 1
    id_partie = generation_id_partie()
    profondeur_reflexion_ia = randint(1, 5)

    level = str(await reader.read(1024)).count("\\x00")

    id_parties.append(id_partie)
    parties[id_partie] = {
        "grille": creation_grille(),
        "jeu_fini": game_finished,
        "etat_jeu": "",
        "level_joueur_0": profondeur_reflexion_ia,
        "level_joueur_1": level,
    }

    try:
        while not game_finished:
            if joueur == 0:
                arbre = Minimax.arbre_possibles(
                    Minimax.Arbre((deepcopy(parties[id_partie]["grille"]), None)),
                    joueur, profondeur_reflexion_ia)

                _, coup = Minimax.minimax(arbre, True, joueur)
                jouer_coup(coup, id_partie, joueur)

            else:
                writer.write(pickle.dumps(parties[id_partie]["grille"]))
                await writer.drain()

                data = await reader.read(1024)
                if not data:
                    break

                coup_joueur_1 = pickle.loads(data)
                jouer_coup(coup_joueur_1, id_partie, joueur)

            if Minimax.victoire(parties[id_partie]["grille"], joueur):
                game_finished = True
                parties[id_partie]["etat_jeu"] = f"Bravo le joueur {int(joueur)} ({Minimax.jetons[joueur]}) a gagné"
                parties[id_partie]["jeu_fini"] = game_finished
                writer.write(b"END")
                await writer.drain()

            compteur += 1
            if compteur == Minimax.largeur * Minimax.hauteur:
                game_finished = True
                parties[id_partie]["etat_jeu"] = "Partie terminée : plus de place sur la grille de jeu."
                parties[id_partie]["jeu_fini"] = game_finished

            await asyncio.sleep(3)

            joueur = not joueur
    except Exception as e:
        print(f"Erreur : {e}")
        parties[id_partie]["jeu_fini"] = True
    finally:
        writer.close()
        await writer.wait_closed()


async def start_tcp_server():
    server = await asyncio.start_server(handle_tcp_client, ip_address, port)
    addr = server.sockets[0].getsockname()
    print(f"Serveur TCP en écoute sur {addr}")
    async with server:
        await server.serve_forever()


async def main():
    await asyncio.gather(
        start_http_server(),
        start_tcp_server(),
    )


asyncio.run(main())

import random
import string

from data.data import data
from player.player import player


# Définition de la fonction main
def main():
    print("MAIN")
    path = r"C:\Users\willi\Documents\Perso\cyber-infra\docker-infra\Template\data.xlsx"
    datastruct = data(path)

    equipe_bleu, equipe_rouge = generer_equipe(datastruct)
    docker_compose_content = generer_docker_compose(equipe_bleu, equipe_rouge)

    # Écrire le contenu dans un fichier docker-compose.yml
    with open(r"C:\Users\willi\Documents\Perso\cyber-infra\docker-infra\Template\dockerCompose\docker-compose.yml", 'w') as file:
        file.write(docker_compose_content)

    print("Le fichier docker-compose.yml a été généré avec succès.")

def generer_equipe(datastruct):
    equipe_bleu = []
    equipe_rouge = []
    port_count = 2222  # Commence à exposer les conteneurs à partir de ce port

    # Création des joueurs de l'équipe Bleue
    for i in range(datastruct.get_nb_bleu()):
        prenom, nom = datastruct.getParticipantBleu(i)
        mots = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        joueur = player(prenom, nom, "", "bleu", port_count, mots)
        equipe_bleu.append(joueur)
        port_count += 1

    # Création des joueurs de l'équipe Rouge
    for i in range(datastruct.get_nb_rouge()):
        prenom, nom = datastruct.getParticipantRouge(i)
        mots = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        joueur = player(prenom, nom, "", "rouge", port_count, mots)
        equipe_rouge.append(joueur)
        port_count += 1

    return equipe_bleu, equipe_rouge

def generer_docker_compose(equipe_bleu, equipe_rouge):
    docker_compose = "version: '3.7'\nservices:\n"
    ssh_pass = "root"
    compteur_bleu = 1
    compteur_rouge = 1

    # Générer les services Ubuntu pour l'équipe Bleue
    for joueur in equipe_bleu:
        docker_compose += (
            f"  ubuntubleu{compteur_bleu}:\n"
            f"    build:\n"
            f"      context: ../Ubuntu\n"
            f"      args:\n"
            f"        SSH_PASS: {joueur.motspass}\n"
            f"    container_name: ubuntu_bleu_{compteur_bleu}\n"
            f"    ports:\n"
            f"      - '{joueur.port}:22'\n"
        )
        compteur_bleu += 1

    # Générer les services Ubuntu pour l'équipe Rouge
    for joueur in equipe_rouge:
        docker_compose += (
            f"  ubunturouge{compteur_rouge}:\n"
            f"    build:\n"
            f"      context: ../Ubuntu\n"
            f"      args:\n"
            f"        SSH_PASS: {joueur.motspass}\n"
            f"    container_name: ubuntu_rouge_{compteur_rouge}\n"
            f"    ports:\n"
            f"      - '{joueur.port}:22'\n"
        )
        compteur_rouge += 1

    # Déclaration du réseau personnalisé "hack réseau"
    docker_compose += (
        "\nnetworks:\n"
        "  reseau:\n"
        "    driver: bridge\n"
    )

    return docker_compose



# Vérification si le script est exécuté directement
if __name__ == "__main__":
    main()
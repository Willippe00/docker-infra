from data.data import data


# Définition de la fonction main
def main():
    print("MAIN")
    path = r"C:\Users\willi\Documents\Perso\cyber-infra\docker-infra\Template\data.xlsx"
    datastruct = data(path)
    docker_compose_content = generer_docker_compose(datastruct)

    # Écrire le contenu dans un fichier docker-compose.yml
    with open(r"C:\Users\willi\Documents\Perso\cyber-infra\docker-infra\Template\dockerCompose\docker-compose.yml", 'w') as file:
        file.write(docker_compose_content)

    print("Le fichier docker-compose.yml a été généré avec succès.")


def generer_docker_compose(datastruct):
    docker_compose = "version: '3.7'\nservices:\n"
    proxy_count = 1
    ssh_pass = "root"
    port_count = 2222  # Commence à exposer les conteneurs à partir de ce port

     # Générer les services Ubuntu pour l'équipe Bleue
    for i in range(1, datastruct.get_nb_bleu() + 1):
        docker_compose += (
            f"  ubuntubleu{i}:\n"
            f"    build:\n"
            f"      context: ../Ubuntu\n"
            f"      args:\n"
            f"        SSH_PASS: {ssh_pass}\n"
            f"    container_name: ubuntu_ssh_Bleu{i}\n"
            f"    ports:\n"
            f"      - '{port_count}:{port_count}'\n"
        )
        port_count += 1  # Incrémente le numéro de port pour le prochain conteneur

    # Générer les services Ubuntu pour l'équipe Rouge
    for i in range(1, datastruct.get_nb_rouge() + 1):
        docker_compose += (
            f"  ubunturouge{i}:\n"
            f"    build:\n"
            f"      context: ../Ubuntu\n"
            f"      args:\n"
            f"        SSH_PASS: {ssh_pass}\n"
            f"    container_name: ubuntu_ssh_Rouge{i}\n"
            f"    ports:\n"
            f"      - '{port_count}:{port_count}'\n"
        )
        port_count += 1  # Continue d'incrémenter le numéro de port pour chaque conteneur

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
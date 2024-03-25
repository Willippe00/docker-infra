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

    # Générer les services Ubuntu pour l'équipe Bleue
    for i in range(1, datastruct.get_nb_bleu() + 1):
        docker_compose += (
            f"  ubuntubleu{i}:\n"
            f"    build: ../Ubuntu\n"
            f"    container_name: ubuntu_ssh_Bleu{i}\n"
        )

    # Générer les services Ubuntu pour l'équipe Rouge
    for i in range(1, datastruct.get_nb_rouge() + 1):
        docker_compose += (
            f"  ubunturouge{i}:\n"
            f"    build: ../Ubuntu\n"
            f"    container_name: ubuntu_ssh_Rouge{i}\n"
        )

    # Générer un service de proxy TCP pour chaque service Ubuntu
    for i in range(1, datastruct.get_nb_bleu() + datastruct.get_nb_rouge() + 1):
        port = 2222 + (proxy_count - 1)
        team = "bleu" if i <= datastruct.get_nb_bleu() else "rouge"
        container_index = i if i <= datastruct.get_nb_bleu() else i - datastruct.get_nb_bleu()
        docker_compose += (
            f"  ssh-proxy{proxy_count}:\n"
            f"    image: tecnativa/tcp-proxy\n"
            f"    environment:\n"
            f"      LISTEN: ':{port}'\n"
            f"      TALK: 'ubuntu{team}{container_index}:22'\n"
            f"    ports:\n"
            f"      - '{port}:{port}'\n"
            f"    depends_on:\n"
            f"      - ubuntu{team}{container_index}\n"
        )
        proxy_count += 1

    return docker_compose

# Vérification si le script est exécuté directement
if __name__ == "__main__":
    main()
from data.data import data

# Définition de la fonction main
def main():
    print("MAIN")
    path = r"C:\Users\willi\Documents\Perso\cyber-infra\docker-infra\Template\data.xlsx"
    datastruct = data(path)
    print(datastruct.getnbBleu())

# Vérification si le script est exécuté directement
if __name__ == "__main__":
    main()
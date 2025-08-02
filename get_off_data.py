import requests


def main():
    get_openfoodfacts_products_dataset()

def get_openfoodfacts_products_dataset():
    """
    Cette fonction permet de récupérer un large jeu de données sans saturer la mémoire RAM,
    grâce à l'utilisation du paramètre stream que la librairie requests. Le fichier CSV est 
    téléchargé et sauvegardé par morceaux avec la methode .iter_content() de la librairie 
    requests, ce qui optimise la gestion des ressources.
    """


    # Réccupération du csv
    url = "https://static.openfoodfacts.org/data/en.openfoodfacts.org.products.csv.gz"
    response = requests.get(url, stream=True)

    # Sauvegarde du csv 
    if response.status_code == 200:
        with open('data/full_openfoodfacts_products_dataset.csv.gz', 'wb') as file:
            for chunck in response.iter_content(chunk_size=8000):
                file.write(chunck)

     

if __name__ == "__main__" :
    main()
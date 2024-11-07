import requests
from requests import HTTPError

class TEST():
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'x-api-key': "05cbbba2-8dcf-4c15-8a8d-cc117924b3f8"
        }
        self.base_url = "https://u32sgtzygj.execute-api.eu-west-3.amazonaws.com/dev/users/"

    def get_user(self, user_id):
        """Récupère les détails d'un utilisateur"""
        try:
            response = self.session.get(
                url=f"{self.base_url}{user_id}/GetUserDetails",
            )
            response.raise_for_status()
            print("Réponse réussie :", response.json())
        except HTTPError as http_err:
            print("Erreur HTTP lors de la requête :", http_err)
        except Exception as err:
            print("Autre erreur lors de la requête :", err)

    def create_user(self):
        """Crée un utilisateur en envoyant une requête POST pour obtenir un token"""
        try:
            # l'envoi d'une requête POST pour obtenir un token ✨
            res = self.session.post(
                url=f"{self.base_url}getToken",  # Utilisation du bon endpoint pour obtenir un token
                json={"email": "kvn.life@gmail.com"}  # Données envoyées (ici l'email)
            )

            res.raise_for_status()  # je check si la requête a échoué (statut HTTP)

            token_data = res.json()

            # je recup la valeur du token (ici 'hash_value')
            new_api_key = token_data.get('hash_value')

            if new_api_key:
                print(f"Token reçu avec succès : {new_api_key}")
                self.session.headers['x-api-key'] = new_api_key  # Met à jour la clé API dans les en-têtes
                print("Nouvelle clé API définie pour les requêtes suivantes.")
            else:
                print("Aucun token trouvé dans la réponse.")

        except HTTPError as http_err:
            print("Erreur HTTP lors de la création de l'utilisateur :", http_err)
        except Exception as err:
            print("Autre erreur lors de la création de l'utilisateur :", err)

    def create_user_with_id(self, user_id, email):
        """Crée un utilisateur avec un ID spécifique"""
        try:
            # Envoie d'une requête POST pour créer un user
            res = self.session.post(
                url=f"{self.base_url}{user_id}/CreateUser",  # Utilisation du bon endpoint pour créer un utilisateur
                json={"email": email}  # Données envoyées (ici l'email)
            )

            res.raise_for_status()  # Vérifie si la requête a échoué (statut HTTP)

            # Récupère la réponse JSON (par exemple, confirmation de la création de l'utilisateur)
            user_data = res.json()
            print("Utilisateur créé avec succès :", user_data)

        except HTTPError as http_err:
            print("Erreur HTTP lors de la création de l'utilisateur :", http_err)
        except Exception as err:
            print("Autre erreur lors de la création de l'utilisateur :", err)

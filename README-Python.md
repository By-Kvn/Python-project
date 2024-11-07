
# 🚀 **Projet Python-AWS-Lambda** 🐍  
**Étudiants ayant bossé arduement sur le projet** :  
**Kevin LABATTE**, **Hamza Idb**  

---

## 📋 **Notes** 📝

Hey Alex ! Après beaucoup d'efforts et de tests, le rendu n'a pas vraiment beaucoup avancé, mais voici ce que le projet contient jusqu'à maintenant :

- ✅ **Lambda GET** : Permet de récupérer les informations d'un utilisateur via une requête GET.
- ✅ **Lambda CREATE** : Permet de créer un utilisateur via une requête POST.
- ✅ **POST pour la création** : Implémentation d'un POST pour créer un utilisateur.
- ✅ **Affichage des ID et emails depuis AWS** : Récupération et affichage des ID et emails d'utilisateurs depuis DynamoDB (référez-vous au screen pour voir l'ajout effectué depuis la console AWS).

---

## ⚡ **Commande pour vérifier l'ID en fonction de l'email**

Pour vérifier l'ID d'un utilisateur à partir de son email, vous pouvez utiliser la commande `curl` suivante :

```bash
curl -X POST https://u32sgtzygj.execute-api.eu-west-3.amazonaws.com/dev/createUser \
-H "Content-Type: application/json" \
-d '{"email": "kevinLBT@gmail.com"}'
```


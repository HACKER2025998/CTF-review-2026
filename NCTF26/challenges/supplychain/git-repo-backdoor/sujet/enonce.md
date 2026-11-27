# git-repo-backdoor

- **Catégorie :** supplychain
- **Auteur :** inconnu (à compléter)
- **Points :** —

## Énoncé

Une archive d'objets Git `acme-service.git(2).tar` contient un dépôt bare avec l'historique de commits, dont `6941af71e2cf0e2f07eb9d2789733cf7385c170d`. Une discussion précédente avait identifié le hook `.githooks/post-checkout` comme mécanisme de porte dérobée, mis en œuvre dans les fichiers versionnés et pouvant être activé lorsque `core.hooksPath` pointe sur le dossier de hooks. Le flag avait été communiqué comme résolu.

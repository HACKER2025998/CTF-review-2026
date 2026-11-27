# leaky-prefix

- **Catégorie :** cloud
- **Auteur :** inconnu (à compléter)
- **Points :** —

## Énoncé

Le bucket fictif `kekeli-media-prod` fournit un index d'objets : `assets/public/...` pour les contenus censés être publics et `assets/public-backup/...` pour un contenu de restauration plus sensible. La politique `bucket-policy.json` doit être analysée en comparant son pattern de ressources à chaque clé d'objet ; une expression de préfixe trop permissive couvre involontairement les backups.

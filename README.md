# Exercice 2 — Transport de containers

## Données

| Dépôt \ Magasin | M1 | M2 | M3 | Offre |
|---|---:|---:|---:|---:|
| D1 | 5 | 3 | 4 | 8 |
| D2 | 6 | 7 | 2 | 9 |
| Demande | 4 | 5 | 8 | 17 |

Les demandes magasins sont 4, 5 et 8 containers.

## Modèle PLNE

min Z = 5x11 + 3x12 + 4x13 + 6x21 + 7x22 + 2x23

sous contraintes d'offre, de demande et xij ∈ ℕ.

## Solution optimale

- D1 → M1 : 3
- D1 → M2 : 5
- D1 → M3 : 0
- D2 → M1 : 1
- D2 → M2 : 0
- D2 → M3 : 8

**Coût total = 52**

## Recherche taboue

- Solution initiale : coin nord-ouest.
- Voisinage : transfert sur un rectangle 2×2 avec δ = ±1.
- Liste taboue : mouvements inverses interdits pendant 5 itérations.
- Critère d'aspiration : acceptation si amélioration du meilleur coût global.

---

# Exercice 3 — Voyageur de commerce

## Matrice des distances

| Ville | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 14 | 15 | - | - | - | - | 17 |
| 2 |  | 13 | 14 | 20 | - | - | 21 |
| 3 |  |  | 11 | 21 | 17 | 9 | 9 |
| 4 |  |  |  | 11 | 10 | 8 | 20 |
| 5 |  |  |  |  | 15 | 18 | - |
| 6 |  |  |  |  |  | 9 | - |
| 7 |  |  |  |  |  |  | 13 |

## Solution initiale

1-2-3-4-5-6-7-8-1

**Coût initial = 103.**

## 1) Recherche taboue

Meilleure tournée trouvée : **1-2-4-5-6-7-3-8-1 — Coût = 98**

## 2) Recuit simulé

5 itérations, avec variation empirique de T.

Meilleure tournée trouvée : **1-2-4-5-6-7-3-8-1 — Coût = 98**

## 3) Algorithme génétique

Meilleure tournée trouvée : **1-2-4-5-6-7-3-8-1 — Coût = 98**

---

# Résultats optimaux

- **Exercice 2** : coût minimal = **52**.
- **Exercice 3** : tournée optimale = **1-2-4-5-6-7-3-8-1**, coût = **98**.
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

# Ordonnancement de maintenance des centrales

## Données

| Unité | Capacité (MW) | Intervalles requis |
|---|---:|---:|
| 1 | 20 | 2 |
| 2 | 15 | 2 |
| 3 | 35 | 1 |
| 4 | 40 | 1 |
| 5 | 15 | 1 |
| 6 | 15 | 1 |
| 7 | 10 | 1 |

Demandes : 80, 90, 65 et 70 MW pour les intervalles 1 à 4.

Capacité totale = 150 MW.

## Encodage

Chaque unité est représentée par un gène de 4 bits.

- `1` : maintenance pendant l’intervalle.
- `0` : pas de maintenance.

Les patterns autorisés sont :

- Unités 1 et 2 : `1100`, `0110`, `0011`
- Unités 3 à 7 : `1000`, `0100`, `0010`, `0001`

Un chromosome est la concaténation des 7 blocs de 4 bits.

## Fonction objective

Pour un chromosome c :

M_t(c) = Σ capacité_i × bit_{i,t}(c)

Réserve_t(c) = 150 − M_t(c) − Demande_t

Performance(c) = max(0, min_t Réserve_t(c))

On maximise Performance(c).

## Contraintes

- La maintenance d’une unité commence au début d’un intervalle et se termine à la fin de l’intervalle.
- Chaque unité doit utiliser un pattern autorisé.
- La réserve doit être positive ; sinon la performance vaut 0.

## Opérateurs génétiques

- Sélection par loterie.
- Croisement sur frontière de blocs de 4 bits.
- Mutation par inversion d’un bloc de 4 bits, avec réparation si le pattern inversé n’est pas autorisé.
- Variante testée : mutation aléatoire d’un bloc par un autre pattern autorisé.
- Élitisme : conservation du meilleur individu.

## Fichier

Le code correspondant se trouve dans `cedule.py`.

Exécution :

```bash
python cedule.py

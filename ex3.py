# ============================================================
# ex3.py — Exercice 3 : Voyageur de commerce (TSP)
# Recherche taboue + Recuit simulé + Algorithme génétique
# ============================================================

import random
import math

INF = 10**9
dist = [
    [0,   14,  15,  INF, INF, INF, INF, 17],
    [14,  0,   13,  14,  20,  INF, INF, 21],
    [15,  13,  0,   11,  21,  17,  9,   9],
    [INF, 14,  11,  0,   11,  10,  8,   20],
    [INF, 20,  21,  11,  0,   15,  18,  INF],
    [INF, INF, 17,  10,  15,  0,   9,   INF],
    [INF, INF, 9,   8,   18,  9,   0,   13],
    [17,  21,  9,   20,  INF, INF, 13,  0]
]
n_tsp = len(dist)


def tour_cost(tour):
    c = 0
    for i in range(n_tsp):
        c += dist[tour[i]][tour[(i + 1) % n_tsp]]
    return c


def tour_str(tour):
    return "-".join(str(v + 1) for v in tour) + "-" + str(tour[0] + 1)


# ---------- 1) Recherche taboue ----------
def tabu_search_tsp(initial_tour, max_iter=100, tenure=5):
    current = initial_tour[:]
    best = current[:]
    best_cost = tour_cost(current)
    tabu = []

    for it in range(max_iter):
        best_neighbor = None
        best_neighbor_cost = float('inf')
        best_move = None

        for i in range(n_tsp):
            city = current[i]
            rest = current[:i] + current[i + 1:]
            for j in range(n_tsp):
                new_tour = rest[:j] + [city] + rest[j:]
                is_tabu = (city, i) in tabu
                c = tour_cost(new_tour)

                if is_tabu and c >= best_cost:
                    continue

                if c < best_neighbor_cost:
                    best_neighbor_cost = c
                    best_neighbor = new_tour
                    best_move = (city, i, j)

        if best_neighbor is None:
            break

        current = best_neighbor
        city, old_pos, new_pos = best_move
        tabu.append((city, old_pos))
        if len(tabu) > tenure:
            tabu.pop(0)

        if best_neighbor_cost < best_cost:
            best_cost = best_neighbor_cost
            best = current[:]

    return best, best_cost


# ---------- 2) Recuit simulé ----------
def simulated_annealing_tsp(initial_tour, iterations=5, T0=10.0, alpha=0.7):
    current = initial_tour[:]
    best = current[:]
    best_cost = tour_cost(current)
    T = T0

    for k in range(iterations):
        i, j = random.sample(range(n_tsp), 2)
        neighbor = current[:]
        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
        neighbor_cost = tour_cost(neighbor)
        delta = neighbor_cost - tour_cost(current)

        if delta < 0 or random.random() < math.exp(-delta / T):
            current = neighbor
            if neighbor_cost < best_cost:
                best = neighbor[:]
                best_cost = neighbor_cost

        T *= alpha

    return best, best_cost


# ---------- 3) Algorithme génétique ----------
def genetic_algorithm_tsp(initial_tour, pop_size=8, generations=50,
                          mutation_rate=0.2):
    def create_individual():
        ind = initial_tour[:]
        random.shuffle(ind)
        return ind

    def order_crossover(parent1, parent2):
        size = len(parent1)
        start, end = sorted(random.sample(range(size), 2))
        child = [-1] * size
        child[start:end + 1] = parent1[start:end + 1]
        pos = (end + 1) % size
        for gene in parent2:
            if gene not in child:
                child[pos] = gene
                pos = (pos + 1) % size
        return child

    def mutate(ind):
        if random.random() < mutation_rate:
            i, j = random.sample(range(len(ind)), 2)
            ind[i], ind[j] = ind[j], ind[i]
        return ind

    population = [create_individual() for _ in range(pop_size)]
    population[0] = initial_tour[:]
    best = min(population, key=tour_cost)
    best_cost = tour_cost(best)

    for gen in range(generations):
        scored = [(tour_cost(ind), ind) for ind in population]
        scored.sort(key=lambda x: x[0])
        new_pop = [scored[0][1][:]]

        while len(new_pop) < pop_size:
            def select():
                a = random.choice(scored)
                b = random.choice(scored)
                return a[1] if a[0] < b[0] else b[1]

            p1 = select()
            p2 = select()
            child = order_crossover(p1, p2)
            child = mutate(child)
            new_pop.append(child)

        population = new_pop
        current_best = min(population, key=tour_cost)
        if tour_cost(current_best) < best_cost:
            best = current_best[:]
            best_cost = tour_cost(best)

    return best, best_cost


# ---------- Lancement Exercice 3 ----------
def ex3_tsp():
    print("\n=== Exercice 3 : Voyageur de commerce ===")
    initial = list(range(n_tsp))
    print("Tournée initiale :", tour_str(initial), "Coût =", tour_cost(initial))

    best_tabu, cost_tabu = tabu_search_tsp(initial, max_iter=100, tenure=5)
    print("\n1) Recherche taboue :")
    print("   Tournée :", tour_str(best_tabu))
    print("   Coût    :", cost_tabu)

    random.seed(42)
    best_sa, cost_sa = simulated_annealing_tsp(initial, iterations=5,
                                               T0=10.0, alpha=0.7)
    print("\n2) Recuit simulé (5 itérations) :")
    print("   Tournée :", tour_str(best_sa))
    print("   Coût    :", cost_sa)

    random.seed(42)
    best_ga, cost_ga = genetic_algorithm_tsp(initial, pop_size=8,
                                             generations=50,
                                             mutation_rate=0.2)
    print("\n3) Algorithme génétique :")
    print("   Tournée :", tour_str(best_ga))
    print("   Coût    :", cost_ga)

    return (best_tabu, cost_tabu), (best_sa, cost_sa), (best_ga, cost_ga)


if __name__ == "__main__":
    ex3_tsp()
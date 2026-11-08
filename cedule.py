import random

# Capacités des 7 unités (MW)
CAP = [20, 15, 35, 40, 15, 15, 10]
# Demandes sur les 4 intervalles
DEM = [80, 90, 65, 70]
TOT = sum(CAP)
T = 4
N = len(CAP)

# Patterns de maintenance autorisés pour chaque unité
# Unités 1 et 2 : 2 intervalles consécutifs
# Unités 3 à 7 : 1 intervalle
PATTERNS = [
    [(1, 1, 0, 0), (0, 1, 1, 0), (0, 0, 1, 1)],
    [(1, 1, 0, 0), (0, 1, 1, 0), (0, 0, 1, 1)],
    [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)],
    [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)],
    [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)],
    [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)],
    [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)],
]


def maintenance(chrom):
    # Puissance totale en maintenance par intervalle
    m = [0] * T
    for i, p in enumerate(chrom):
        for t in range(T):
            if p[t]:
                m[t] += CAP[i]
    return m


def reserves(chrom):
    # Réserve nette par intervalle
    m = maintenance(chrom)
    return [TOT - m[t] - DEM[t] for t in range(T)]


def fitness(chrom):
    # Performance = plus petite réserve, bornée à 0
    return max(0, min(reserves(chrom)))


def random_chrom():
    # Chromosome aléatoire : un pattern autorisé par unité
    return [random.choice(PATTERNS[i]) for i in range(N)]


def roulette(pop):
    # Sélection par loterie (proportionnelle au fitness)
    vals = [fitness(c) for c in pop]
    total = sum(vals)
    if total == 0:
        return random.choice(pop)
    r = random.random() * total
    s = 0
    for c, v in zip(pop, vals):
        s += v
        if s >= r:
            return c
    return pop[-1]


def crossover(p1, p2):
    # Croisement sur frontière de blocs de 4 bits
    cut = random.randint(1, N - 1)
    c1 = p1[:cut] + p2[cut:]
    c2 = p2[:cut] + p1[cut:]
    return c1, c2


def mutation_inversion(chrom):
    # Mutation par inversion d'un bloc de 4 bits
    chrom = chrom[:]
    i = random.randrange(N)
    rev = tuple(reversed(chrom[i]))
    # On répare si le pattern inversé n'est pas autorisé
    chrom[i] = rev if rev in PATTERNS[i] else random.choice(PATTERNS[i])
    return chrom


def mutation_random(chrom):
    # Mutation aléatoire : remplace un bloc par un autre pattern autorisé
    chrom = chrom[:]
    i = random.randrange(N)
    chrom[i] = random.choice(PATTERNS[i])
    return chrom


def ga(pop_size=70, generations=200, pc=0.8, pm=0.2,
       mutation=mutation_inversion, seed=42):
    random.seed(seed)
    # Population initiale
    pop = [random_chrom() for _ in range(pop_size)]
    best = max(pop, key=fitness)
    best_fit = fitness(best)

    for _ in range(generations):
        # Élitisme : on garde le meilleur
        new_pop = [best[:]]

        while len(new_pop) < pop_size:
            # Sélection par loterie
            p1 = roulette(pop)
            p2 = roulette(pop)

            # Croisement
            if random.random() < pc:
                c1, c2 = crossover(p1, p2)
            else:
                c1, c2 = p1[:], p2[:]

            # Mutation
            if random.random() < pm:
                c1 = mutation(c1)
            if random.random() < pm:
                c2 = mutation(c2)

            new_pop.append(c1)
            if len(new_pop) < pop_size:
                new_pop.append(c2)

        pop = new_pop
        # Mise à jour du meilleur global
        cur = max(pop, key=fitness)
        if fitness(cur) > best_fit:
            best = cur[:]
            best_fit = fitness(cur)

    return best, best_fit


def chrom_str(chrom):
    # Affichage lisible : blocs de 4 bits séparés par un espace
    return " ".join("".join(str(b) for b in p) for p in chrom)


if __name__ == "__main__":
    # Test avec mutation par inversion
    best, f = ga(mutation=mutation_inversion)
    print("Mutation par inversion")
    print("Cédule :", chrom_str(best))
    print("Maintenance :", maintenance(best))
    print("Réserve :", reserves(best))
    print("Performance :", f)

    # Test avec mutation aléatoire
    best2, f2 = ga(mutation=mutation_random)
    print("\nMutation aléatoire")
    print("Cédule :", chrom_str(best2))
    print("Maintenance :", maintenance(best2))
    print("Réserve :", reserves(best2))
    print("Performance :", f2)
# ============================================================
# ex2.py — Exercice 2 : Transport de containers
# Recherche taboue
# ============================================================

def ex2_transport():
    cost = [
        [5, 3, 4],
        [6, 7, 2]
    ]
    supply = [8, 9]
    demand = [4, 5, 8]
    n = len(supply)
    m = len(demand)

    def total_cost(x):
        return sum(cost[i][j] * x[i][j] for i in range(n) for j in range(m))

    def initial_solution():
        """Solution réalisable par coin nord-ouest."""
        x = [[0] * m for _ in range(n)]
        s = supply[:]
        d = demand[:]
        i = j = 0
        while i < n and j < m:
            q = min(s[i], d[j])
            x[i][j] = q
            s[i] -= q
            d[j] -= q
            if s[i] == 0:
                i += 1
            if d[j] == 0:
                j += 1
        return x

    def neighbors(x):
        """Voisins par transfert sur un rectangle 2x2 (delta = ±1)."""
        for i1 in range(n):
            for i2 in range(i1 + 1, n):
                for j1 in range(m):
                    for j2 in range(j1 + 1, m):
                        for delta in (1, -1):
                            y = [row[:] for row in x]
                            y[i1][j1] += delta
                            y[i1][j2] -= delta
                            y[i2][j1] -= delta
                            y[i2][j2] += delta
                            if all(y[i][j] >= 0 for i in range(n) for j in range(m)):
                                yield y, (i1, j1, i2, j2, delta)

    def tabu_search(max_iter=100, tenure=5):
        x = initial_solution()
        best = [row[:] for row in x]
        best_cost = total_cost(x)
        tabu = []

        for it in range(max_iter):
            best_neighbor = None
            best_neighbor_cost = float('inf')
            best_move = None

            for y, move in neighbors(x):
                c = total_cost(y)
                inverse = (move[0], move[1], move[2], move[3], -move[4])
                is_tabu = inverse in tabu

                # critère d'aspiration
                if is_tabu and c >= best_cost:
                    continue

                if c < best_neighbor_cost:
                    best_neighbor_cost = c
                    best_neighbor = y
                    best_move = move

            if best_neighbor is None:
                break

            x = best_neighbor
            inverse = (best_move[0], best_move[1], best_move[2],
                       best_move[3], -best_move[4])
            tabu.append(inverse)
            if len(tabu) > tenure:
                tabu.pop(0)

            if best_neighbor_cost < best_cost:
                best_cost = best_neighbor_cost
                best = [row[:] for row in x]

        return best, best_cost

    best_x, best_c = tabu_search()
    print("=== Exercice 2 : Transport ===")
    print("Solution optimale trouvée :")
    for row in best_x:
        print(row)
    print("Coût total :", best_c)
    return best_x, best_c


if __name__ == "__main__":
    ex2_transport()
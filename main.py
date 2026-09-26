from collections import Counter

from mapa import Mapa
from algoritmos.bfs import bfs
from algoritmos.ucs import ucs
from algoritmos.greedy import greedy


print("=== PRUEBA BFS ===")

grilla_bfs = [
    "#######",
    "#.....#",
    "#.....#",
    "#...S.#",
    "#######"
]

mapa_bfs = Mapa(grilla_bfs)

ocupacion_bfs = Counter({
    (2, 1): 3
})

ruta_bfs = bfs(
    mapa_bfs,
    (1, 1),
    mapa_bfs.salida,
    ocupacion_bfs
)

print(ruta_bfs)


print("\n=== PRUEBA UCS ===")

grilla_ucs = [
    "###########",
    "#........S#",
    "#.#######.#",
    "#.........#",
    "###########"
]

mapa_ucs = Mapa(grilla_ucs)

ocupacion_ucs = Counter({
    (1, 2): 3,
    (1, 3): 3,
    (1, 4): 3,
    (1, 5): 3,
    (1, 6): 3,
    (1, 7): 3,
    (1, 8): 3
})

ruta_ucs = ucs(
    mapa_ucs,
    (1, 1),
    mapa_ucs.salida,
    ocupacion_ucs
)

print(ruta_ucs)


print("\n=== PRUEBA GREEDY ===")

grilla_greedy = [
    "#####",
    "#...#",
    "#...#",
    "#..S#",
    "#####"
]

mapa_greedy = Mapa(grilla_greedy)

ocupacion_greedy = Counter({
    (2, 1): 3
})

ruta_greedy = greedy(
    mapa_greedy,
    (1, 1),
    mapa_greedy.salida,
    ocupacion_greedy
)

print(ruta_greedy)
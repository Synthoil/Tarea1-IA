from collections import Counter

from mapa import Mapa
from algoritmos.bfs import bfs
from algoritmos.ucs import ucs


grilla = [
    "###########",
    "#........S#",
    "#.#######.#",
    "#.........#",
    "###########"
]

mapa = Mapa(grilla)

inicio = (1, 1)

ocupacion = Counter({
    (1, 2): 3,
    (1, 3): 3,
    (1, 4): 3,
    (1, 5): 3,
    (1, 6): 3,
    (1, 7): 3,
    (1, 8): 3
})


ruta_bfs = bfs(
    mapa,
    inicio,
    mapa.salida,
    ocupacion
)

ruta_ucs = ucs(
    mapa,
    inicio,
    mapa.salida,
    ocupacion
)


print("Ruta BFS:")
print(ruta_bfs)

print("\nRuta UCS:")
print(ruta_ucs)
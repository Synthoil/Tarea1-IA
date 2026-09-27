from collections import Counter

from mapa import Mapa
from algoritmos.ucs import ucs
from algoritmos.astar import astar


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


ruta_ucs = ucs(
    mapa,
    inicio,
    mapa.salida,
    ocupacion
)

ruta_astar = astar(
    mapa,
    inicio,
    mapa.salida,
    ocupacion
)


print("Ruta UCS:")
print(ruta_ucs)

print("\nRuta A*:")
print(ruta_astar)
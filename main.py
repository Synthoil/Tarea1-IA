from mapa import Mapa


grilla = [
    "##########",
    "#........#",
    "#..###...#",
    "#....F...#",
    "#......S.#",
    "##########"
]


mapa = Mapa(grilla)

print("Mapa inicial:")
mapa.mostrar()

print("\nSalida:")
print(mapa.salida)

print("\nFuego:")
print(mapa.fuego)

print("\nVecinos desde (1, 1):")
print(mapa.obtener_vecinos((1, 1)))
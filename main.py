from mapa import Mapa
from agente import Agente
from simulacion import Simulacion
from algoritmos.bfs import bfs


grilla = [
    "##########",
    "#........#",
    "#..###...#",
    "#........#",
    "#......S.#",
    "##########"
]


mapa = Mapa(grilla)


agentes = [
    Agente(1, (1, 1)),
    Agente(2, (1, 2)),
    Agente(3, (1, 3))
]

for agente in agentes:
    ruta = bfs(
        mapa,
        agente.posicion,
        mapa.salida
    )

    print(f"Agente {agente.id}: {ruta}")


simulacion = Simulacion(
    mapa,
    agentes,
    bfs
)


for i in range(10):
    simulacion.ejecutar_turno()

    print(f"Turno {simulacion.turno}")

    for agente in agentes:
        print(
            f"Agente {agente.id}: "
            f"posicion={agente.posicion}, "
            f"evacuado={agente.evacuado}, "
            f"vivo={agente.vivo}"
        )

    print()

    if simulacion.terminada():
        break
import random

from mapa import Mapa
from agente import Agente
from simulacion import Simulacion

from escenarios import MAPA_1

from algoritmos.bfs import bfs
from algoritmos.ucs import ucs
from algoritmos.greedy import greedy
from algoritmos.astar import astar


ALGORITMOS = {
    "BFS": bfs,
    "UCS": ucs,
    "Greedy": greedy,
    "A*": astar
}


CUELLOS_BOTELLA = [
    (10, 11),
    (12, 11)
]


def crear_agentes(posiciones):
    return [
        Agente(i + 1, posicion)
        for i, posicion in enumerate(posiciones)
    ]


for nombre, algoritmo in ALGORITMOS.items():

    print("\n======================================")
    print(nombre)
    print("======================================")

    random.seed(42)

    mapa = Mapa(MAPA_1["grilla"])
    agentes = crear_agentes(MAPA_1["agentes"])

    simulacion = Simulacion(
        mapa,
        agentes,
        algoritmo
    )

    max_esperando = 0
    max_ocupacion_cuello = 0

    while not simulacion.terminada():

        simulacion.ejecutar_turno()

        ocupacion = simulacion.obtener_ocupacion()

        esperando = sum(
            1
            for agente in simulacion.agentes_activos()
            if agente.turnos_esperando > 0
        )

        ocupacion_cuello = sum(
            ocupacion[posicion]
            for posicion in CUELLOS_BOTELLA
        )

        max_esperando = max(
            max_esperando,
            esperando
        )

        max_ocupacion_cuello = max(
            max_ocupacion_cuello,
            ocupacion_cuello
        )

        print(
            f"Turno {simulacion.turno:2d} | "
            f"Cuello 1: {ocupacion[(10, 11)]} | "
            f"Cuello 2: {ocupacion[(12, 11)]} | "
            f"Esperando: {esperando:2d} | "
            f"Activos: {len(simulacion.agentes_activos()):2d}"
        )

    print("\nResumen:")
    print(f"Evacuados: {simulacion.evacuados}")
    print(f"Muertos: {simulacion.muertos}")
    print(f"Máximo de agentes esperando: {max_esperando}")
    print(f"Máxima ocupación total en cuellos: {max_ocupacion_cuello}")
    print(f"Último evacuado: {simulacion.turno_ultimo_evacuado}")
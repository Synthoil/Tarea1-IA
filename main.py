import random
import statistics

from mapa import Mapa
from agente import Agente
from simulacion import Simulacion

from escenarios import MAPA_1, MAPA_2, MAPA_3

from algoritmos.bfs import bfs
from algoritmos.ucs import ucs
from algoritmos.greedy import greedy
from algoritmos.astar import astar


ITERACIONES = 20


ALGORITMOS = {
    "BFS": bfs,
    "UCS": ucs,
    "Greedy": greedy,
    "A*": astar
}


ESCENARIOS_PRUEBA = [
    {
        "escenario": MAPA_1,
        "fuegos_extra": [
            (9, 25),
            (13, 5),
            (18, 25)
        ]
    },
    {
        "escenario": MAPA_2,
        "fuegos_extra": [
            (3, 25),
            (9, 2),
            (18, 25)
        ]
    },
    {
        "escenario": MAPA_3,
        "fuegos_extra": [
            (3, 25),
            (10, 2),
            (18, 25)
        ]
    }
]


def crear_agentes(posiciones):
    return [
        Agente(i + 1, posicion)
        for i, posicion in enumerate(posiciones)
    ]


def agregar_fuegos(grilla, posiciones):
    nueva_grilla = [
        list(fila)
        for fila in grilla
    ]

    for fila, columna in posiciones:
        if nueva_grilla[fila][columna] == ".":
            nueva_grilla[fila][columna] = "F"

    return [
        "".join(fila)
        for fila in nueva_grilla
    ]


def ejecutar_simulacion(
    escenario,
    algoritmo,
    semilla,
    fuegos_extra
):
    rng_fuego = random.Random(semilla)
    rng_movimientos = random.Random(
        semilla + 100000
    )

    grilla = agregar_fuegos(
        escenario["grilla"],
        fuegos_extra
    )

    mapa = Mapa(
        grilla,
        rng=rng_fuego
    )

    agentes = crear_agentes(
        escenario["agentes"]
    )

    simulacion = Simulacion(
        mapa,
        agentes,
        algoritmo,
        rng=rng_movimientos
    )

    return simulacion.ejecutar()


for prueba in ESCENARIOS_PRUEBA:

    escenario = prueba["escenario"]
    fuegos_extra = prueba["fuegos_extra"]

    print("\n======================================")
    print(escenario["nombre"])
    print("4 focos iniciales")
    print("======================================")

    for nombre, algoritmo in ALGORITMOS.items():

        supervivencias = []
        tiempos = []

        for semilla in range(ITERACIONES):

            resultado = ejecutar_simulacion(
                escenario,
                algoritmo,
                semilla,
                fuegos_extra
            )

            supervivencia = (
                resultado["evacuados"]
                / resultado["agentes_totales"]
                * 100
            )

            supervivencias.append(
                supervivencia
            )

            if resultado["turno_ultimo_evacuado"] is not None:
                tiempos.append(
                    resultado["turno_ultimo_evacuado"]
                )

        print(
            f"{nombre}: "
            f"supervivencia={statistics.mean(supervivencias):.1f}% | "
            f"min={min(supervivencias):.1f}% | "
            f"max={max(supervivencias):.1f}% | "
            f"tiempo={statistics.mean(tiempos):.1f}"
        )
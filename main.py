import random

from mapa import Mapa
from agente import Agente
from simulacion import Simulacion

from escenarios import MAPA_1, MAPA_2, MAPA_3

from algoritmos.bfs import bfs
from algoritmos.ucs import ucs
from algoritmos.greedy import greedy
from algoritmos.astar import astar
from algoritmos.genetico import genetico


ALGORITMOS = {
    "1": ("BFS", bfs),
    "2": ("UCS", ucs),
    "3": ("Greedy", greedy),
    "4": ("A*", astar),
    "5": ("Genético", genetico)
}


ESCENARIOS = {
    "1": MAPA_1,
    "2": MAPA_2,
    "3": MAPA_3
}


def crear_agentes(posiciones):
    return [
        Agente(i + 1, posicion)
        for i, posicion in enumerate(posiciones)
    ]


def generar_posiciones_agentes(
    escenario,
    rng_posiciones
):
    grilla = escenario["grilla"]
    zona = escenario["zona_inicio"]

    posiciones_validas = []

    for fila in range(
        zona["fila_min"],
        zona["fila_max"] + 1
    ):
        for columna in range(
            zona["columna_min"],
            zona["columna_max"] + 1
        ):
            if grilla[fila][columna] == ".":
                posiciones_validas.append(
                    (fila, columna)
                )

    cantidad = escenario["cantidad_agentes"]

    return rng_posiciones.sample(
        posiciones_validas,
        cantidad
    )


def ejecutar_simulacion(
    escenario,
    algoritmo,
    semilla
):
    rng_fuego = random.Random(
        semilla
    )

    rng_posiciones = random.Random(
        semilla + 50000
    )

    rng_movimientos = random.Random(
        semilla + 100000
    )

    rng_genetico = random.Random(
        semilla + 150000
    )

    mapa = Mapa(
        escenario["grilla"],
        rng=rng_fuego
    )

    posiciones = generar_posiciones_agentes(
        escenario,
        rng_posiciones
    )

    agentes = crear_agentes(
        posiciones
    )

    if algoritmo is genetico:
        rng_algoritmo = rng_genetico
    else:
        rng_algoritmo = None

    simulacion = Simulacion(
        mapa,
        agentes,
        algoritmo,
        rng=rng_movimientos,
        rng_algoritmo=rng_algoritmo
    )

    return simulacion.ejecutar()


def main():
    print("====================================")
    print("       ESCAPE DE LA TORRE")
    print("====================================")

    print("\nSeleccione un mapa:")
    print("1. Alta densidad / Cuello de botella")
    print("2. Densidad media / Laberinto corporativo")
    print("3. Baja densidad / Dispersion abierta")

    opcion_mapa = input("\nMapa: ")

    if opcion_mapa not in ESCENARIOS:
        print("Opcion de mapa invalida.")
        return

    print("\nSeleccione un algoritmo:")
    print("1. BFS")
    print("2. UCS")
    print("3. Greedy")
    print("4. A*")
    print("5. Genetico")

    opcion_algoritmo = input("\nAlgoritmo: ")

    if opcion_algoritmo not in ALGORITMOS:
        print("Opcion de algoritmo invalida.")
        return

    entrada_semilla = input(
        "\nSemilla (Enter para usar 0): "
    )

    if entrada_semilla == "":
        semilla = 0
    else:
        semilla = int(entrada_semilla)

    escenario = ESCENARIOS[
        opcion_mapa
    ]

    nombre_algoritmo, algoritmo = (
        ALGORITMOS[opcion_algoritmo]
    )

    print("\nEjecutando simulacion...")
    print(
        f"Mapa: {escenario['nombre']}"
    )
    print(
        f"Algoritmo: {nombre_algoritmo}"
    )
    print(
        f"Agentes: "
        f"{escenario['cantidad_agentes']}"
    )
    print(
        f"Semilla: {semilla}"
    )

    resultado = ejecutar_simulacion(
        escenario,
        algoritmo,
        semilla
    )

    total = resultado[
        "agentes_totales"
    ]

    evacuados = resultado[
        "evacuados"
    ]

    muertos = resultado[
        "muertos"
    ]

    atrapados = (
        total
        - evacuados
        - muertos
    )

    supervivencia = (
        evacuados
        / total
        * 100
    )

    print("\n====================================")
    print("             RESULTADOS")
    print("====================================")

    print(
        f"Agentes totales: {total}"
    )

    print(
        f"Evacuados: {evacuados}"
    )

    print(
        f"Fallecidos: {muertos}"
    )

    print(
        f"Atrapados: {atrapados}"
    )

    print(
        f"Supervivencia: "
        f"{supervivencia:.2f}%"
    )

    print(
        f"Turnos de simulacion: "
        f"{resultado['turnos_simulacion']}"
    )

    print(
        f"Ultimo evacuado: "
        f"{resultado['turno_ultimo_evacuado']}"
    )


if __name__ == "__main__":
    main()
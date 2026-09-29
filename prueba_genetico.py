import random
import time
import statistics

from mapa import Mapa
from escenarios import MAPA_1, MAPA_2, MAPA_3

from algoritmos.genetico import genetico
from algoritmos.bfs import bfs


SEMILLAS = 20


PRUEBAS = [
    {
        "nombre": "Mapa 1 - Alta densidad",
        "escenario": MAPA_1,
        "inicios": [
            (1, 2),
            (3, 29),
            (7, 1),
            (6, 25),
            (2, 15),
        ],
    },

    {
        "nombre": "Mapa 2 - Densidad media",
        "escenario": MAPA_2,
        "inicios": [
            (2, 1),
            (4, 16),
            (9, 23),
            (13, 16),
            (7, 13),
        ],
    },

    {
        "nombre": "Mapa 3 - Baja densidad",
        "escenario": MAPA_3,
        "inicios": [
            (14, 9),
            (2, 7),
            (6, 12),
            (13, 5),
            (18, 4),
        ],
    },
]


def probar_posicion(mapa, inicio):
    objetivo = mapa.salida
    ocupacion = {}

    ruta_bfs = bfs(
        mapa,
        inicio,
        objetivo,
        ocupacion
    )

    if ruta_bfs is None:
        longitud_bfs = None
    else:
        if ruta_bfs[0] == inicio:
            longitud_bfs = len(ruta_bfs) - 1
        else:
            longitud_bfs = len(ruta_bfs)

    longitudes_genetico = []
    completas = 0
    parciales = 0
    sin_ruta = 0

    inicio_tiempo = time.perf_counter()

    for semilla in range(SEMILLAS):
        rng = random.Random(semilla)

        ruta = genetico(
            mapa,
            inicio,
            objetivo,
            ocupacion,
            rng
        )

        if ruta is None:
            sin_ruta += 1
            continue

        if ruta[-1] == objetivo:
            completas += 1
            longitudes_genetico.append(
                len(ruta)
            )
        else:
            parciales += 1

    tiempo_total = (
        time.perf_counter()
        - inicio_tiempo
    )

    print()
    print(f"Inicio: {inicio}")
    print(f"Salida: {objetivo}")

    if longitud_bfs is not None:
        print(
            f"Longitud BFS: {longitud_bfs}"
        )
    else:
        print(
            "BFS no encontro ruta"
        )

    print(
        f"Completas: {completas}/{SEMILLAS}"
    )

    print(
        f"Parciales: {parciales}"
    )

    print(
        f"Sin ruta: {sin_ruta}"
    )

    if longitudes_genetico:

        promedio = statistics.mean(
            longitudes_genetico
        )

        print(
            f"Longitud genetico media: "
            f"{promedio:.2f}"
        )

        print(
            f"Longitud genetico min/max: "
            f"{min(longitudes_genetico)} / "
            f"{max(longitudes_genetico)}"
        )

        if longitud_bfs is not None:

            diferencia = (
                promedio
                - longitud_bfs
            )

            print(
                f"Diferencia media respecto BFS: "
                f"{diferencia:.2f}"
            )

    print(
        f"Tiempo para {SEMILLAS} pruebas: "
        f"{tiempo_total:.3f}s"
    )

    return {
        "completas": completas,
        "parciales": parciales,
        "sin_ruta": sin_ruta,
    }


def main():

    total_pruebas = 0
    total_completas = 0
    total_parciales = 0
    total_sin_ruta = 0

    tiempo_inicio = time.perf_counter()

    for prueba in PRUEBAS:

        print()
        print("=" * 55)
        print(prueba["nombre"])
        print("=" * 55)

        mapa = Mapa(
            prueba["escenario"]["grilla"]
        )

        for inicio in prueba["inicios"]:

            resultado = probar_posicion(
                mapa,
                inicio
            )

            total_pruebas += SEMILLAS

            total_completas += (
                resultado["completas"]
            )

            total_parciales += (
                resultado["parciales"]
            )

            total_sin_ruta += (
                resultado["sin_ruta"]
            )

    tiempo_total = (
        time.perf_counter()
        - tiempo_inicio
    )

    print()
    print("=" * 55)
    print("RESUMEN FINAL")
    print("=" * 55)

    porcentaje_exito = (
        total_completas
        / total_pruebas
        * 100
    )

    print(
        f"Ejecuciones totales: "
        f"{total_pruebas}"
    )

    print(
        f"Rutas completas: "
        f"{total_completas}"
    )

    print(
        f"Rutas parciales: "
        f"{total_parciales}"
    )

    print(
        f"Sin ruta: "
        f"{total_sin_ruta}"
    )

    print(
        f"Tasa de exito: "
        f"{porcentaje_exito:.2f}%"
    )

    print(
        f"Tiempo total: "
        f"{tiempo_total:.3f}s"
    )


if __name__ == "__main__":
    main()
import csv 
import random
import statistics

from mapa import Mapa
from agente import Agente
from simulacion import Simulacion
from escenarios import ESCENARIOS

from algoritmos.bfs import bfs
from algoritmos.ucs import ucs
from algoritmos.greedy import greedy
from algoritmos.astar import astar 
from algoritmos.genetico import genetico

ITERACIONES = 120   

ALGORITMOS = {
    "BFS": bfs,
    "UCS": ucs,
    "Greedy": greedy,
    "A*": astar,
    "Genetico": genetico
}


def crear_agentes(posiciones):
    return [
        Agente(i + 1, posicion)
        for i, posicion in enumerate(posiciones)
    ]
    
    
def generar_posiciones_agentes(escenario, rng_posiciones):
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

    if len(posiciones_validas) < cantidad:
        raise ValueError(
            "No hay suficientes posiciones validas "
            "para crear los agentes."
        )

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

    resultado = simulacion.ejecutar()

    return resultado


def calcular_metricas(resultados):
    supervivencias = []
    tiempos = []
    
    total_evacuados = 0
    total_muertos = 0
    total_atrapados = 0
    
    corridas_sin_sobrevivientes = 0
    
    for resultado in resultados:
        total = resultado["agentes_totales"]
        evacuados = resultado["evacuados"]
        muertos = resultado["muertos"]
        
        atrapados = total - evacuados - muertos
        
        supervivencia = (
            evacuados / total 
        ) * 100
        
        supervivencias.append(supervivencia)
        
        total_evacuados += evacuados
        total_muertos += muertos
        total_atrapados += atrapados
        
        tiempo = resultado["turno_ultimo_evacuado"]
        
        if tiempo is not None:
            tiempos.append(tiempo)
        else:
            corridas_sin_sobrevivientes += 1
            
    metricas = {
        "supervivencia_media": statistics.mean(supervivencias),
        "supervivencia_min": min(supervivencias),
        "supervivencia_max": max(supervivencias),

        "evacuados_totales": total_evacuados,
        "muertos_totales": total_muertos,
        "atrapados_totales": total_atrapados,
        
        "corridas_sin_sobrevivientes":
            corridas_sin_sobrevivientes
    }
    
    if tiempos:
        metricas["tiempo_media"] = statistics.mean(tiempos)

        metricas["tiempo_desviacion"] = (
            statistics.pstdev(tiempos)
        )

        metricas["tiempo_min"] = min(tiempos)
        metricas["tiempo_max"] = max(tiempos)

    else:
        metricas["tiempo_media"] = None
        metricas["tiempo_desviacion"] = None
        metricas["tiempo_min"] = None
        metricas["tiempo_max"] = None

    return metricas


def ejecutar_benchmark():
    resumen = []
    
    for escenario in ESCENARIOS:
        
        print("\n==========================================")
        print(escenario["nombre"])
        print("==========================================")
        
        for nombre_algoritmo, algoritmo in ALGORITMOS.items():
            
            resultados = []
            
            
            for semilla in range(ITERACIONES):
                
                resultado = ejecutar_simulacion(
                    escenario,
                    algoritmo,
                    semilla
                )
                
                resultados.append(resultado)
                
                
            metricas = calcular_metricas(resultados)
    
            
            print(f"\n{nombre_algoritmo}")
            print(
                f"Supervivencia media: "
                f"{metricas['supervivencia_media']:.2f}%"
            )
            print(
                f"Supervivencia min/max: "
                f"{metricas['supervivencia_min']:.2f}% / "
                f"{metricas['supervivencia_max']:.2f}%"
            )
            
            if metricas["tiempo_media"] is not None:
                print(
                    f"Tiempo medio: "
                    f"{metricas['tiempo_media']:.2f}"
                )
                print(
                    f"Desviacion estandar: "
                    f"{metricas['tiempo_desviacion']:.2f}"
                )
                print(
                    f"Tiempo min/max: "
                    f"{metricas['tiempo_min']} / "
                    f"{metricas['tiempo_max']}"
                )
                
                print(
                    f"Corridas sin sobrevivientes: "
                    f"{metricas['corridas_sin_sobrevivientes']}"
                )

            resumen.append({
                "mapa": escenario["nombre"],
                "algoritmo": nombre_algoritmo,
                "iteraciones": ITERACIONES,

                "supervivencia_media":
                    metricas["supervivencia_media"],

                "supervivencia_min":
                    metricas["supervivencia_min"],

                "supervivencia_max":
                    metricas["supervivencia_max"],

                "tiempo_media":
                    metricas["tiempo_media"],

                "tiempo_desviacion":
                    metricas["tiempo_desviacion"],

                "tiempo_min":
                    metricas["tiempo_min"],

                "tiempo_max":
                    metricas["tiempo_max"],

                "evacuados_totales":
                    metricas["evacuados_totales"],

                "muertos_totales":
                    metricas["muertos_totales"],

                "atrapados_totales":
                    metricas["atrapados_totales"],
                
                "corridas_sin_sobrevivientes":
                    metricas["corridas_sin_sobrevivientes"],
            })
    
    return resumen


def guardar_csv(resultados):
    nombre_archivo = "benchmark_resultados.csv"

    campos = [
        "mapa",
        "algoritmo",
        "iteraciones",
        "supervivencia_media",
        "supervivencia_min",
        "supervivencia_max",
        "tiempo_media",
        "tiempo_desviacion",
        "tiempo_min",
        "tiempo_max",
        "evacuados_totales",
        "muertos_totales",
        "atrapados_totales",
        "corridas_sin_sobrevivientes"
    ]

    with open(
        nombre_archivo,
        "w",
        newline="",
        encoding="utf-8"
    ) as archivo:

        writer = csv.DictWriter(
            archivo,
            fieldnames=campos
        )

        writer.writeheader()
        writer.writerows(resultados)

    print(
        f"\nResultados guardados en "
        f"{nombre_archivo}"
    )


if __name__ == "__main__":
    resultados = ejecutar_benchmark()

    guardar_csv(resultados)
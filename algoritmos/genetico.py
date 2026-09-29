import random


TAM_POBLACION = 50
GENERACIONES = 40
LONGITUD_CROMOSOMA = 60

PROB_MUTACION = 0.05
PROB_MOVIMIENTO_GUIADO = 0.6

TAM_TORNEO = 3

MOVIMIENTOS = ["U", "D", "L", "R"]


def aplicar_movimiento(posicion, movimiento):
    fila, columna = posicion

    if movimiento == "U":
        return (fila - 1, columna)

    if movimiento == "D":
        return (fila + 1, columna)

    if movimiento == "L":
        return (fila, columna - 1)

    if movimiento == "R":
        return (fila, columna + 1)

    return posicion


def distancia_manhattan(posicion, objetivo):
    return (
        abs(posicion[0] - objetivo[0])
        + abs(posicion[1] - objetivo[1])
    )


def movimientos_validos(mapa, posicion):
    validos = []

    for movimiento in MOVIMIENTOS:
        nueva_posicion = aplicar_movimiento(
            posicion,
            movimiento
        )

        if mapa.es_transitable(nueva_posicion):
            validos.append(movimiento)

    return validos


def generar_individuo(mapa, inicio, objetivo, rng):
    individuo = []

    posicion = inicio

    for _ in range(LONGITUD_CROMOSOMA):

        if posicion == objetivo:
            break

        validos = movimientos_validos(
            mapa,
            posicion
        )

        if not validos:
            break

        if rng.random() < PROB_MOVIMIENTO_GUIADO:

            mejor_distancia = float("inf")
            mejores_movimientos = []

            for movimiento in validos:

                nueva_posicion = aplicar_movimiento(
                    posicion,
                    movimiento
                )

                distancia = distancia_manhattan(
                    nueva_posicion,
                    objetivo
                )

                if distancia < mejor_distancia:
                    mejor_distancia = distancia
                    mejores_movimientos = [
                        movimiento
                    ]

                elif distancia == mejor_distancia:
                    mejores_movimientos.append(
                        movimiento
                    )

            movimiento = rng.choice(
                mejores_movimientos
            )

        else:
            movimiento = rng.choice(
                validos
            )

        individuo.append(movimiento)

        posicion = aplicar_movimiento(posicion, movimiento)

    return individuo


def generar_poblacion(mapa, inicio, objetivo, rng):
    poblacion = []

    for _ in range(TAM_POBLACION):

        individuo = generar_individuo(mapa, inicio, objetivo, rng)

        poblacion.append(individuo)

    return poblacion


def evaluar_individuo(individuo, mapa, inicio, objetivo, ocupacion):
    posicion = inicio

    costo_congestion_total = 0
    cantidad_movimientos_validos = 0

    llega_al_objetivo = False
    hubo_choque = False

    for movimiento in individuo:

        nueva_posicion = aplicar_movimiento(posicion, movimiento)

        if not mapa.es_transitable(
            nueva_posicion
        ):
            hubo_choque = True
            break

        posicion = nueva_posicion
        cantidad_movimientos_validos += 1

        costo_congestion_total += (
            mapa.costo_congestion(
                posicion,
                ocupacion
            ) - 1
        )

        if posicion == objetivo:
            llega_al_objetivo = True
            break

    distancia_final = distancia_manhattan(
        posicion,
        objetivo
    )

    if llega_al_objetivo:

        fitness = (
            10000
            - cantidad_movimientos_validos * 10
            - costo_congestion_total * 5
        )

    else:

        penalizacion_choque = (
            200 if hubo_choque else 0
        )

        fitness = (
            1000
            - distancia_final * 20
            - cantidad_movimientos_validos * 2
            - costo_congestion_total * 5
            - penalizacion_choque
        )

    return fitness


def evaluar_poblacion(poblacion, mapa, inicio, objetivo, ocupacion):
    fitness = []

    for individuo in poblacion:

        valor = evaluar_individuo(individuo, mapa, inicio, objetivo, ocupacion)

        fitness.append(valor)

    return fitness


def seleccion_torneo(poblacion, fitness, rng):
    indices = rng.sample(
        range(len(poblacion)),
        min(
            TAM_TORNEO,
            len(poblacion)
        )
    )

    mejor_indice = indices[0]

    for indice in indices[1:]:

        if fitness[indice] > fitness[mejor_indice]:
            mejor_indice = indice

    return poblacion[mejor_indice][:]


def cruzar(padre1, padre2, rng):
    longitud = min(len(padre1), len(padre2))

    if longitud < 2:
        return padre1[:]

    punto = rng.randint(
        1,
        longitud - 1
    )

    hijo = (
        padre1[:punto]
        + padre2[punto:]
    )

    return hijo


def mutar(individuo, rng):
    mutado = individuo[:]

    for i in range(len(mutado)):

        if rng.random() < PROB_MUTACION:

            movimiento_actual = mutado[i]

            opciones = [
                movimiento
                for movimiento in MOVIMIENTOS
                if movimiento != movimiento_actual
            ]

            mutado[i] = rng.choice(
                opciones
            )

    return mutado


def evolucionar(poblacion, fitness, rng):
    nueva_poblacion = []

    mejor_indice = max(
        range(len(poblacion)),
        key=lambda i: fitness[i]
    )

    mejor_individuo = poblacion[
        mejor_indice
    ][:]

    nueva_poblacion.append(
        mejor_individuo
    )

    while len(nueva_poblacion) < TAM_POBLACION:

        padre1 = seleccion_torneo(poblacion, fitness, rng)
        padre2 = seleccion_torneo(poblacion, fitness, rng)

        hijo = cruzar(padre1, padre2, rng)
        hijo = mutar(hijo, rng)

        nueva_poblacion.append(hijo)

    return nueva_poblacion


def movimientos_a_ruta(individuo, mapa, inicio, objetivo):
    ruta = []

    posicion = inicio

    for movimiento in individuo:

        nueva_posicion = aplicar_movimiento(
            posicion,
            movimiento
        )

        if not mapa.es_transitable(
            nueva_posicion
        ):
            break

        ruta.append(
            nueva_posicion
        )

        posicion = nueva_posicion

        if posicion == objetivo:
            break

    return ruta


def genetico(mapa, inicio, objetivo, ocupacion=None, rng=None):
    if inicio == objetivo:
        return []

    if rng is None:
        rng = random

    poblacion = generar_poblacion(mapa, inicio, objetivo, rng)

    mejor_individuo = None
    mejor_fitness = float("-inf")

    for _ in range(GENERACIONES):

        fitness = evaluar_poblacion(poblacion, mapa, inicio, objetivo, ocupacion)

        for i in range(len(poblacion)):

            if fitness[i] > mejor_fitness:

                mejor_fitness = fitness[i]

                mejor_individuo = poblacion[
                    i
                ][:]

        poblacion = evolucionar(poblacion, fitness, rng)

    fitness = evaluar_poblacion(poblacion, mapa, inicio, objetivo, ocupacion)

    for i in range(len(poblacion)):

        if fitness[i] > mejor_fitness:

            mejor_fitness = fitness[i]

            mejor_individuo = poblacion[
                i
            ][:]

    if mejor_individuo is None:
        return None

    ruta = movimientos_a_ruta(mejor_individuo, mapa, inicio, objetivo)
    if not ruta:
        return None

    return ruta
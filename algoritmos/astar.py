import heapq

def heuristica_manhattan(posicion, objetivo):
    fila, columna = posicion
    fila_objetivo, columna_objetivo = objetivo
    
    return (
        abs(fila - fila_objetivo)
        + abs (columna - columna_objetivo)
    )
    

def astar(mapa, inicio, objetivo, ocupacion=None):
    frontera = []
    
    costo_inicial = 0
    heuristica_inicial = heuristica_manhattan(
        inicio,
        objetivo
    )
    
    heapq.heappush(
        frontera,
        (
            costo_inicial + heuristica_inicial,
            costo_inicial,
            inicio
        )
    )
    
    costos = {
        inicio: 0
    }
    
    padres = {
        inicio: None
    }
    
    while frontera:
        _, costo_actual, actual = heapq.heappop(frontera)
        
        if costo_actual > costos[actual]:
            continue
        
        if actual == objetivo:
            return reconstruir_ruta(
                padres,
                objetivo
            )
            
        for vecino in mapa.obtener_vecinos(actual):
            
            nuevo_costo = (
                costo_actual
                + mapa.costo_congestion(
                    vecino,
                    ocupacion
                )
            )
            
            if (
                vecino not in costos
                or nuevo_costo < costos[vecino]
            ):
                costos[vecino] = nuevo_costo
                padres[vecino] = actual
                
                heuristica = heuristica_manhattan(
                    vecino,
                    objetivo
                )
                
                prioridad = nuevo_costo + heuristica
                
                heapq.heappush(
                    frontera,
                    (
                        prioridad,
                        nuevo_costo,
                        vecino
                    )
                )
    
    return None


def reconstruir_ruta(padres, objetivo):
    ruta = []
    actual = objetivo

    while actual is not None:
        ruta.append(actual)
        actual = padres[actual]

    ruta.reverse()

    return ruta
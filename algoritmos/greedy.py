import heapq


def heuristica_manhattan(posicion, objetivo):
    fila, columna = posicion
    fila_objetivo, columna_objetivo = objetivo
    
    return(
        abs(fila - fila_objetivo)
        + abs(columna - columna_objetivo)
    )
    
    
def greedy(mapa, inicio, objetivo, ocupacion=None):
    frontera = []
    
    heapq.heappush(
        frontera,
        (
            heuristica_manhattan(inicio, objetivo),
            mapa.costo_congestion(inicio, ocupacion),
            inicio
        )
    )
    
    padres = {
        inicio: None
    }
    
    visitados = set()
    
    while frontera:
        _, _, actual = heapq.heappop(frontera)
        
        if actual in visitados:
            continue
        
        visitados.add(actual)
        
        if actual == objetivo:
            return reconstruir_ruta(padres, objetivo)
        
        for vecino in mapa.obtener_vecinos(actual):
            
            if vecino not in visitados and vecino not in padres:
                padres[vecino] = actual
                
                prioridad = heuristica_manhattan(
                    vecino,
                    objetivo
                )
                
                congestion = mapa.costo_congestion(
                    vecino,
                    ocupacion
                )
                
                heapq.heappush(
                    frontera,
                    (
                        prioridad,
                        congestion,
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
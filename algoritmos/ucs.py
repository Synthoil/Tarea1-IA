import heapq

def costo_celda(posicion, ocupacion):
    if ocupacion is None:
        return 1
    
    cantidad = ocupacion.get(posicion, 0)
    
    return 1 + cantidad ** 2


def ucs(mapa, inicio, objetivo, ocupacion=None):
    frontera = []
    
    heapq.heappush(frontera, (0, inicio))
    
    costos = {
        inicio: 0
    }
    
    padres = {
        inicio: None
    }
    
    while frontera:
        costo_actual, actual = heapq.heappop(frontera)
        
        if costo_actual > costos[actual]:
            continue
        
        if actual == objetivo:
            return reconstruir_ruta(padres, objetivo)
        
        for vecino in mapa.obtener_vecinos(actual):
            
            nuevo_costo = (
                costo_actual
                + costo_celda(vecino, ocupacion)
            )
            
            if (
                vecino not in costos
                or nuevo_costo < costos[vecino]
            ):
                costos[vecino] = nuevo_costo
                padres[vecino] = actual
                
                heapq.heappush(
                    frontera,
                    (nuevo_costo, vecino)
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
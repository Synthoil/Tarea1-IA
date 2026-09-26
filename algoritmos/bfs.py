from collections import deque

def bfs(mapa, inicio, objetivo, ocupacion=None):
    cola = deque([inicio])
    
    padres = {
        inicio: None
    }
    
    while cola:
        actual = cola.popleft()
        
        if actual == objetivo:
            return reconstruir_ruta(padres, objetivo)
        
        for vecino in mapa.obtener_vecinos(actual):
            if vecino not in padres:
                padres[vecino] = actual
                cola.append(vecino)
                
    return None

def reconstruir_ruta(padres, objetivo): 
    ruta = []
    actual = objetivo
    
    while actual is not None:
        ruta.append(actual)
        actual = padres[actual]
        
    ruta.reverse()
    
    return ruta
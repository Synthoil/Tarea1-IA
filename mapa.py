import random
from config import PROB_PROPAGACION

class Mapa:
    def __init__(self, grilla):
        self.grilla = [list(fila) for fila in grilla]
        
        self.filas = len(self.grilla)
        self.columnas = len(self.grilla[0])
        
        self.salida = None 
        self.fuego = set()
        
        self.buscar_elementos()
        
        
    def buscar_elementos(self):
        for fila in range(self.filas):
            for columna in range(self.columnas):
                
                celda = self.grilla[fila][columna]
                
                if celda == "S":
                    self.salida = (fila, columna)
                    
                elif celda == "F":
                    self.fuego.add((fila, columna))
                    
                    
    def mostrar(self):
        for fila in self.grilla:
            print("".join(fila))
    
    
    def dentro_del_mapa(self, posicion):
        fila, columna = posicion
        
        return (
            0 <= fila < self.filas
            and 0 <= columna < self.columnas
        )
        
        
    def es_transitable(self, posicion):
        if not self.dentro_del_mapa(posicion):
            return False
        
        fila, columna = posicion
        celda = self.grilla[fila][columna]
        
        return celda != "#" and posicion not in self.fuego
    
    
    def obtener_vecinos(self, posicion):
        fila, columna = posicion
        
        movimientos = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
        ]
        
        vecinos = []
        
        for df, dc in movimientos:
            nueva_posicion = (fila + df, columna + dc)
            
            if self.es_transitable(nueva_posicion):
                vecinos.append(nueva_posicion)
                
        return vecinos
    
    
    def costo_congestion(self, posicion, ocupacion):
        if ocupacion is None:
            return 1
        
        cantidad = ocupacion.get(posicion, 0)
        
        return 1 + cantidad ** 2
    
    
    def propagar_fuego(self):
        nuevo_fuego = set()
        
        for posicion in self.fuego:
            fila, columna = posicion
            
            vecinos = [
                (fila - 1, columna),
                (fila + 1, columna),
                (fila, columna - 1),
                (fila, columna + 1)
            ]
            
            for vecino in vecinos:
                
                if not self.dentro_del_mapa(vecino):
                    continue
                
                fila_vecino, columna_vecino = vecino
                celda = self.grilla[fila_vecino][columna_vecino]
                
                if celda == "#":
                    continue
                if celda == "S":
                    continue
                if vecino in self.fuego:
                    continue
                if random.random() < PROB_PROPAGACION:
                    nuevo_fuego.add(vecino)
        
        for fila, columna in nuevo_fuego:
            self.grilla[fila][columna] = "F"
            
        self.fuego.update(nuevo_fuego)
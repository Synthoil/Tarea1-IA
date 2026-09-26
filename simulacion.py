import random
from collections import Counter

from config import (
    CAPACIDAD_CELDA,
    CAPACIDAD_SALIDA,
    K_FUEGO,
    MAX_ESPERA,
    MAX_TURNOS
)

class Simulacion:
    
    def __init__(self, mapa, agentes, planificador=None):
        self.mapa = mapa
        self.agentes = agentes
        
        self.planificador = planificador
        
        self.turno = 0
        
        self.evacuados = 0
        self.muertos = 0
        
        self.turno_ultimo_evacuado = None
        
    
    def agentes_activos(self):
        return [
            agente 
            for agente in self.agentes 
            if agente.esta_activo()
        ]
        
    
    def obtener_ocupacion(self):
        posiciones = [
            agente.posicion
            for agente in self.agentes_activos()
        ]
        
        return Counter(posiciones)
    
    
    def ruta_necesita_recalculo(self, agente):
        if not agente.ruta:
            return True
        
        siguiente = agente.siguiente_posicion()
        
        if not self.mapa.es_transitable(siguiente):
            return True
        if agente.turnos_esperando >= MAX_ESPERA:
            return True
        
        return False
    
    
    def recalcular_ruta(self, agente):
        if self.planificador is None:
            return
        
        ocupacion = self.obtener_ocupacion()
        
        nueva_ruta =self.planificador(
            self.mapa,
            agente.posicion,
            self.mapa.salida,
            ocupacion
        )
        
        if nueva_ruta is not None:
            agente.asignar_ruta(nueva_ruta)
        else:
            agente.ruta = []
            
    
    def planificar_movimientos(self):
        movimientos = {}
        
        for agente in self.agentes_activos():
            
            if self.ruta_necesita_recalculo(agente):
                self.recalcular_ruta(agente)
                
            movimientos[agente.id] = agente.siguiente_posicion()
            
        return movimientos
    
    
    def procesar_salida(self, movimientos):
        candidatos = []
        
        for agente in self.agentes_activos():
            
            destino = movimientos[agente.id]
            
            if destino == self.mapa.salida:
                candidatos.append(agente)
                
        random.shuffle(candidatos)
        
        pueden_salir = candidatos[:CAPACIDAD_SALIDA]
        
        for agente in pueden_salir:
            agente.evacuar()
            
            self.evacuados += 1
            self.turno_ultimo_evacuado = self.turno
            
        for agente in candidatos[CAPACIDAD_SALIDA:]:
            agente.esperar()
            
        return {agente.id for agente in candidatos}
    
    
    def procesar_movimientos(self, movimientos, procesados_salida):
        ocupacion = self.obtener_ocupacion()
        
        agentes = self.agentes_activos()
        random.shuffle(agentes)
        
        for agente in agentes:
            
            if agente.id in procesados_salida:
                continue
            
            destino = movimientos[agente.id]
            
            if destino == agente.posicion:
                agente.esperar()
                continue
            
            if not self.mapa.es_transitable(destino):
                agente.esperar()
                continue
            
            if ocupacion[destino] >= CAPACIDAD_CELDA:
                agente.esperar()
                continue
            
            posicion_anterior = agente.posicion
            
            ocupacion[posicion_anterior] -= 1
            ocupacion[destino] += 1
            
            agente.mover(destino)
            
            
    def revisar_muertes(self):
        for agente in self.agentes_activos():
                
            if agente.posicion in self.mapa.fuego:
                agente.morir()
                self.muertos += 1
                    
                    
    def ejecutar_turno(self):
        self.turno += 1
            
        movimientos = self.planificar_movimientos()
            
        procesados_salida = self.procesar_salida(movimientos)
            
        self.procesar_movimientos(
            movimientos,
            procesados_salida
        )
            
        if self.turno % K_FUEGO == 0:
            self.mapa.propagar_fuego()
                
        self.revisar_muertes()
            
            
    def terminada(self):
        return len(self.agentes_activos()) == 0
        
        
    def ejecutar(self):
        while not self.terminada() and self.turno < MAX_TURNOS:
            self.ejecutar_turno()
                
        return {
            "agentes_totales": len(self.agentes),
            "evacuados": self.evacuados,
            "muertos": self.muertos,
            "turnos_simulacion": self.turno,
            "turno_ultimo_evacuado": self.turno_ultimo_evacuado
        }
            
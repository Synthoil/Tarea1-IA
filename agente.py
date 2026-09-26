class Agente:
    def __init__(self, id_agente, posicion):
        self.id = id_agente
        self.posicion = posicion
        
        self.ruta = []
        
        self.vivo = True
        self.evacuado = False
        
        self.turnos_esperando = 0
    
    def esta_activo(self):
        return self.vivo and not self.evacuado
    

    def asignar_ruta(self, ruta):
        self.ruta = list(ruta)
        
        if self.ruta and self.ruta[0] == self.posicion:
            self.ruta.pop(0)
            
        
    def siguiente_posicion(self):
        if not self.ruta:
            return self.posicion
        
        return self.ruta[0]
    
    
    def mover(self, nueva_posicion):
        self.posicion = nueva_posicion
        
        if self.ruta and self.ruta[0] == nueva_posicion:
            self.ruta.pop(0)
            
        self.turnos_esperando += 0
        
        
    def esperar(self):
        self.turnos_esperando += 1
        
    
    def morir(self):
        self.vivo = False
        self.ruta = []
        
        
    def evacuar(self):
        self.evacuado = True
        self.ruta = []
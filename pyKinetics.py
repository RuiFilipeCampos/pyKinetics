# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 15:02:47 2020

@author: Rui Campos
"""

"""
VERS 0.0.4 - ainda nao esta disponivel no repositorio pyPI
"""


class Compartimento:
    def __init__(self, initial_condition, name = "NaN"):
        """
        Argumentos
            initial_condition
                valor inicial do compartimento
            name = "NaN"
                nome do compartimento (usado para o label do plot)
        """
        
        self.simulated = False
        self.initial_condition = initial_condition
        
        self.name = name
        self.y = initial_condition
        self.t = 0
        
        self.yAxis = [initial_condition]
        self.tAxis = [self.t]
        
        self.into  = []
        self.out   = []
    
    
    def Y(self):
        return self.y
    
    def reset(self):
        self.y = self.initial_condition
        self.t = 0
        self.yAxis = [self.initial_condition]
        self.tAxis = [self.t]
    
    def connect(self, other, constant, direction = -1):
        """
        Conecta dois compartimentos.
        ----------------------------
            A.connect(B, rate) :: A -> B      com lambda = rate
        ----------------------------
        """
        
        
        
        
        if direction == +1:
            if callable(constant): 
                constant_into = constant
            else: 
                constant_into = lambda : constant
                
            self.into += [(other, constant_into)]
            
            
        if direction == -1:
            if callable(constant) : 
                constant_outo = lambda : -1*constant()
            else: 
                constant_outo = lambda : -1*constant

            self.out += [(self, constant_outo)]
            other.connect(self, constant,  direction = 1)

    def dydt(self, k):
        dYdT = 0
        
        for connection in self.into:
            comp, rate = connection
            dYdT += rate()*(comp.y + k)
        
        for connection in self.out:
            comp, rate = connection
            dYdT += (comp.y + k)*rate()
        return dYdT
    
    def _getChange(self, dt):
        
        k1 = self.dydt(0) * dt
        k2 = self.dydt(k1*.5)*dt
        k3 = self.dydt(k2*.5)*dt
        k4 = self.dydt(k3)*dt
        
        return k1, k2, k3, k4
    
    def _change_state(self, k, dt):
        self.y += 1/6 * (k[0] + 2*k[1] + 2*k[2] + k[3])
        self.yAxis += [self.y]
        
        self.t += dt
        self.tAxis += [self.t]


    
    def plot(self):
        if self.simulated is False:
            raise RuntimeError("Compartimento ainda não foi simulado.")
        
        import matplotlib.pyplot as plt
        
        plt.plot(self.tAxis, self.yAxis, label=self.name)
        
        
        
class Model:
    def __init__(self, *args):
        """
        USAGE
            Model(A, B, C, ...) onde {A, B, C, ...} são compartimentos.
        """
        self.entities = args
        self.simulated = False
        
    def __iter__(self):
        yield from self.entities
    
    def reset(self):
        self.simulated = False
        for comp in self:
            comp.reset()
    
    def introduce_decay(self, rate):
        """
        Introduz uma "saída" em todos os compartimentos. Com o mesmo rate.
        """
        
        decay = Compartimento(0, name="decay")
        for entity in self.entities:
            entity.connect(decay, rate)
        
    def introduce_exit(self, exit_point, rate):
        """
        Introduzir saída num compartimento específico.
        """
        
        exit = Compartimento(0, name = "exit")
        exit_point.connect(exit, rate)
        
        
    def run(self, tf, N):
        """
        Correr simulação.
        PARÂMETROS
            tf :: tempo final - simulação corre entre 0 e tf
            N  :: número de pontos
        """
        
        if self.simulated is True:
            raise RuntimeError("Simulação já foi feita.")
        
        dt = tf/N
        
        changes = [0]*len(self.entities)
    
        for _ in range(N):
            for i, comp in enumerate(self):
                changes[i] = comp._getChange(dt)
    
            for i, comp in enumerate(self):
                comp._change_state(changes[i], dt)
    
        self.simulated = True
        
        for comp in self:
            comp.simulated = True
                
    def plot(self, size = (10, 10)):
        """
        Gráfico da simulação.
        """
        
        if self.simulated is False:
            raise RuntimeError("Simulação ainda não foi feita.")
        
        fig = figure(figsize = size)
        for comp in self.entities:
            comp.plot()
            legend()
            
            
            
class Model:
    """
    USAGE
        model = Model(A, B, C, ...) onde A, B, C, ... são objetos da classe Compartimento
    """
    def __init__(self, *args):
        self.entities = args
        self.simulated = False
        
    def __iter__(self):
        yield from self.entities
    
    def reset(self):
        self.simulated = False
        for comp in self:
            comp.reset()
    
    def introduce_decay(self, rate):
        """
        Introduz uma "saída" em todos os compartimentos. Com o mesmo rate.
        """
        
        decay = Compartimento(0, name="decay")
        for entity in self.entities:
            entity.connect(decay, rate)
        
    def introduce_exit(self, exit_point, rate):
        """
        Introduzir saída num compartimento específico.
        """
        
        exit = Compartimento(0, name = "exit")
        exit_point.connect(exit, rate)
        
        
    def run(self, tf, N):
        """
        Correr simulação.
        PARÂMETROS
            tf :: tempo final - simulação corre entre 0 e tf
            N  :: número de pontos
        """
        
        if self.simulated is True:
            raise RuntimeError("Simulação já foi feita.")
        
        dt = tf/N
        
        changes = [0]*len(self.entities)
    
        for _ in range(N):
            for i, comp in enumerate(self):
                changes[i] = comp._getChange(dt)
    
            for i, comp in enumerate(self):
                comp._change_state(changes[i], dt)
    
        self.simulated = True
        
        for comp in self:
            comp.simulated = True
                
    def plot(self, size = (10, 10)):
        """
        Gráfico da simulação.
        """
        
        if self.simulated is False:
            raise RuntimeError("Simulação ainda não foi feita.")
        
        fig = figure(figsize = size)
        for comp in self.entities:
            comp.plot()
            legend()

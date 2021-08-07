# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 15:02:47 2020

@author: Rui Campos
"""

"""
VERS 0.0.4 - ainda nao esta disponivel no repositorio pyPI
"""
from numpy import *
from matplotlib.pyplot import *

class Entity:
    def __init__(self, initial_condition, name = "Untitled"):
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
    
    def __repr__(self):
        sim = "simulated" if self.simulated else "not simulated" 
        return f"<Entity({sim}): {self.name}; Initial Value: {self.initial_condition}>"
    
    def Y(self):
        return self.y
    
    def reset(self):
        self.y = self.initial_condition
        self.t = 0
        self.yAxis = [self.initial_condition]
        self.tAxis = [self.t]
    

    def __rshift__(self, other):
        """
        Connects instance to other, and returns itself.
        >>> A >> B
        A
        

        """
        self.connect(other)
        return other

    def __lshift__(self, other):
        """
        
        >>> A << B
        B
        """
        other.connect(self)
        return self

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
        
    


def lock(func):
    def new_method(*args, **kwargs):
        
        self = args[0]
        if self.simulated:
            raise RuntimeError("> Cannot do that! Simulation has been ran. (use `.reset` method")

        return func(*args, **kwargs)
    return new_method
            
class Model:
    """Instances of `Model` represent the model you have created.
    These instances will manage the simulation.
    
    USAGE
    >>> A = Entity(1); B = Entity(0);
    >>> A.connect(B)
    >>> model = Model(A, B) # use as many as you like, Model(A, B, C, ...)
    >>> model.run(10, 1000)

    """
    def __init__(self, *args, name = "Untitled Model"):
        """Initialize `Model` instance.

        >>> model = Model(A, B, C, D, ..., name = "My Model!")
        """

        self.entities = args
        self.simulated = False
        self.name = name
        self.exits = []
        
    def __iter__(self):
        yield from self.entities
    
    def reset(self):
        self.simulated = False
        for comp in self:
            comp.reset()
    

    @lock
    def introduce_decay(self, rate):
        """Introduces a decay on all entities.
        """
        
        decay = Entity(0, name="decay")
        for entity in self.entities:
            entity.connect(decay, rate)
    
    @lock
    def introduce_exit(self, entity, rate):
        """Connects `entity` to an exit compartment.
        """
        
        exit = Entity(0, name = f"Exit #{len(self.exits)+1}")
        self.exits.append(exit)

        entity.connect(exit, rate)
        
    @lock
    def run(self, time = 10, Np = 1000):
        """
        Correr simulação.
        PARÂMETROS
            tf :: tempo final - simulação corre entre 0 e tf
            N  :: número de pontos
        """
        tf = time
        N = Np
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
        """Plot the result of the simulation.
        """
        
        if not self.simulated:
            raise RuntimeError("> No data. Please run the simulation first.")

        fig = figure(figsize = size)
        for comp in self.entities:
            comp.plot()
            legend()
        xlabel("Time (A.U.)")
        ylabel("Ammount of stuff in entity (A.U.)")
        title(self.name)
        show()

    def create_figure(self, size = (10, 10)):
        """Creates matplotlib figure and returns it.
        """
        
        if not self.simulated:
            raise RuntimeError("> No data. Please run the simulation first.")

        fig = figure(figsize = size)
        for comp in self.entities:
            comp.plot()
            legend()

        title(self.name)
        return fig

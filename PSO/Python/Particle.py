import math
import random
import numpy as np
from Problem import Problem
from sklearn.preprocessing import MinMaxScaler

class Particle( Problem ):

    def __init__( self, apply_local_consistency = True ):
        super().__init__(apply_local_consistency)

        self.x = []
        self.v = [ 0 for x in range(self.n_vars) ]
        
        self.fill_x_array()
        self.p = self.x.copy()
    
    def fill_x_array( self ):
        new_x_values = []

        for domain in self.domains:
            new_x_values.append(random.randint(self.domains[domain][0], self.domains[domain][-1]))
        self.x = new_x_values
    
    def move( self , g, theta, alpha, beta ):
        for index in range( 0, self.n_vars ): 
            self.v[index] = ( self.v[index] * theta ) + ( alpha * random.uniform(0, 1) * ( g.p[index] - self.x[index] ) ) + ( beta * random.uniform(0, 1) * ( self.p[index] - self.x[index] ) )
            if index == (len(self.x) - 1):#para y1
                self.x[index] = self.__to_discreet( self.x[index] + self.v[index], self.domains["y1"] )
            else:#se tuvo que agregar un valor aleatorio extra en base al dominio de la variable para mejorar la exploracion del algoritmo
                self.x[index] = self.__to_discreet( self.x[index] + self.v[index], self.domains[f'x{index + 1}'] )

    def is_feasible( self ):
        return self.check_constraint(self.x)
    
    def compute_values_fitness( self ):
        return self.compute_fitness(self.x)
    
    def compute_values_fitness_p_best( self ):
        return self.compute_fitness(self.p)
    
    def is_better_than( self, g ):
        return self.compute_values_fitness() > g.compute_values_fitness()
    
    def is_better_than_p_best( self ):
        return self.compute_values_fitness() > self.compute_values_fitness_p_best()
    
    def update_p_best( self ):
        self.p = self.x.copy()
        
    def copy( self, object ):
        if ( isinstance(object, Particle) ):
            self.x = object.x.copy()
            self.p = object.p.copy()
            self.v = object.v.copy()
            self.domains = object.domains.copy()
    
    def __to_discreet( self, x: float, domain: list[int] ):#utiliza metodo de aceptacion y rechazo? - simulacion - mejorar
        #pasar n dominios y dividirlos en n partes y seleccionarlos en base al valor de sigmoide
        #probabilidad de seleccion (posicion): 1/n, n = cantidad de elementos => p_individual(x_{i})
        #valor de la sigmoide: s_y = p_acumulada(x_{i}) => i = ?; i = round(p_acumulada(x_{i})/p_individual(x_{i}), 0) - existe un pequeño error por el redondeo 50/50?
        #valor de x para un conjunto de n valores: x = n[i - 1] y se retorna

        #Se necesita hacer transformacion de valores de x para adecuarlos al resultado entregado por la sigmoide

        #Se realiza re-escalamiento de los datos y al x de entrada, con un valor minimo de -4.2 y un valor maximode 4.2 
        #para dar como resultado en la funcion sigmoide un valor minimo de 0 y un valor maximo de 1
        values = np.arange(domain[0], domain[1] + 1)
        scaler = MinMaxScaler(feature_range = (-4.2, 4.2))
        scaler.fit(values.reshape(-1, 1))
        scaled_x_value = scaler.data_max_ if scaler.transform([[x]]) > scaler.data_max_ else scaler.transform([[x]])

        individual_p = 1/len(values)
        accumulated_p = (1 / (1 + math.pow(math.e, -scaled_x_value)))
        variable_position = int(round(accumulated_p/individual_p, 0))
        #se necesita agregar más aleatoridad a la seleccion de variable, por ello se realiza lo siguiente homologando al to_binary eseñado
        return random.randint(domain[0], domain[1] if variable_position == len(values) else values[variable_position])

import math
import random
import numpy as np
from Problem import Problem
from sklearn.preprocessing import MinMaxScaler

class Salp( Problem ):

    def __init__( self, apply_local_consistency = True ):
        super().__init__(apply_local_consistency)
        self.x = []
        self.aux = 0

        self.fill_x_array()
    
    def fill_x_array( self ):
        new_x_values = []

        for domain in self.domains:
            new_x_values.append(random.randint(self.domains[domain][0], self.domains[domain][-1]))
        self.x = new_x_values

    def leader_move( self, food, c1 ):
        for index in range( 0, self.n_vars ):
            c2 = random.uniform(0, 1)
            c3 = random.uniform(0, 1)

            if index == (len(self.x) - 1):#para y1
                domain = self.domains["y1"]
                ub, lb = domain[-1], domain[0]
            else:
                domain = self.domains[f'x{index + 1}']
                ub, lb = domain[-1], domain[0]
            
            self.x[index] = self.__to_discreet( food.x[index] + c1*((ub - lb)*c2 + lb) if c3 >= 0 else food.x[index] - c1*((ub - lb)*c2 + lb), domain )

    def follower_move( self , previus_follower ):
        for index in range( 0, self.n_vars ):       
            if index == (len(self.x) - 1):#para y1
                self.x[index] = self.__to_discreet( 0.5*( self.x[index] + previus_follower.x[index] ), self.domains["y1"] )
            else:#se tuvo que agregar un valor aleatorio extra en base al dominio de la variable para mejorar la exploracion del algoritmo
                self.x[index] = self.__to_discreet( 0.5*( self.x[index] + previus_follower.x[index] ) + random.randint(self.domains[f'x{index + 1}'][0], self.domains[f'x{index + 1}'][1]),  self.domains[f'x{index + 1}'] )
    
    def is_feasible( self ):
        return self.check_constraint(self.x)
    
    def compute_values_fitness( self ):
        self.aux += 1
        return self.compute_fitness(self.x)
    
    def is_better_than( self, g ):
        return self.compute_values_fitness() > g.compute_values_fitness()
    
    def copy( self, object ):
        if ( isinstance(object, Salp) ):
            self.x = object.x.copy()
            self.domains = object.domains.copy()

    def __to_discreet( self, x: float, domain: list[int] ):
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
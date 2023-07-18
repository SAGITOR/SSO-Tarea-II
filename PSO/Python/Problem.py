import numpy as np

class Problem:
    def __init__ ( self, apply_local_consistency = True ): #secuencial
        self.n_vars = 6
        self.domains = {#no se puede hacer por limite superior en inferior, no todos los dominios son intervalos continuos?
            'x1': [0, 15], 
            'x2': [0, 10], 
            'x3': [0, 25], 
            'x4': [0, 4], 
            'x5': [0, 30], 
            'y1': [0, 1]
        } #x_j
        self.arcos = [
            ('x1', 'x2'), ('x2', 'x1'), #Gastos maximos anuncions tv
            ('x1_2', 'x2_2'), ('x2_2', 'x1_2'), #Cantidad anuncios maximos tv
            ('x2', 'y1'), ('y1', 'x2'), #Invertir en tv noche - necesario?
            ('x3', 'y1'), ('y1', 'x3'), #Invertir en diario - necesario?
        ]
        self.constraints = {
            ('x1', 'x2'): lambda x1, x2: 150*x1 <= 1800 - 300*x2,
            ('x2', 'x1'): lambda x2, x1: 1800 - 300*x2 >= 150*x1,
            ('x1_2', 'x2_2'): lambda x1, x2: x1 <= 20 - x2,
            ('x2_2', 'x1_2'): lambda x2, x1: 20 - x2 >= x1,
            ('x2', 'y1'): lambda x2, y1: x2 <= 10*(1 - y1),
            ('y1', 'x2'): lambda y1, x2: 10*(1 - y1) >= x2,
            ('x3', 'y1'): lambda x3, y1: x3 <= 25*y1,
            ('y1', 'x3'): lambda y1, x3: 25*y1 >= x3
        }
        if ( apply_local_consistency ):
            self.arco_consistencia()

    def compute_fitness(self, bin: list):#Comprobar el valor en una funcion multi-objetivo - priorizar la minimizacion con las restricciones existentes da una mala solucion
        return ((65*bin[0] + 90*bin[1] + 40*bin[2] + 60*bin[3] + 20*bin[4])/2153.33)*0.6 + ((3006.67 - (150*bin[0] + 300*bin[1] + 40*bin[2] + 100*bin[3] + 10*bin[4]))/3006.67)*0.4
    
    def check_constraint(self, x: list):#Restricciones
        if ( 150*x[0] + 300*x[1] <= 1800 and x[0] + x[1] <= 20 and x[1] <= 10*(1 - x[5]) and x[2] <= 25*x[5] and 1000*x[0] + 2000*x[1] + 1500*x[2] + 2500*x[3] + 300*x[4] <= 50000 ):
            return True
        
        return False
            
    def arco_consistencia(self):#arco-consistencia
        queue = self.arcos[:]
        while queue:
            (x, y) = queue.pop(0)
            revised = self.__revise_arco_consistencia(x, y)#cambiar por solo self en [parametros]
            if revised:
                neighbors = [neighbor for neighbor in self.arcos if neighbor[1] == x]
                queue = queue + neighbors

    def __revise_arco_consistencia(self, x, y):
        revised = False
        y_domain = self.domains[y.split("_")[0]]
        x_domain = list(range(self.domains[x.split("_")[0]][0], self.domains[x.split("_")[0]][-1] + 1))
        all_constraints = [ constraint for constraint in self.constraints if constraint[0] == x and constraint[1] == y ]
        
        for x_value in x_domain.copy():
            satisfies = False

            for y_value in range(y_domain[0], y_domain[-1] + 1):
                for constraint in all_constraints:
                    constraint_func = self.constraints[constraint]
                    if constraint_func(x_value, y_value):
                        satisfies = True

            if not satisfies:
                x_domain.remove(x_value)
                revised = True
                
        self.domains[x.split("_")[0]] = [x_domain[0], x_domain[-1]]
        return revised
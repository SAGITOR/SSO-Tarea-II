import math
from Salp import Salp

class Swarm:
    def __init__( self ):
        self.ps = 25
        self.swarm = []
        self.food = None
        self.MaxIter = 400
        self.bestPoint = 0
        self.optimum = 0.676286850565496

    def execute( self ):
        self.__init_rand()
        self.__evolve()

    def __rpd( self ):
        return round(self.__difference() / self.optimum * 100, 2)
    
    def __difference( self ):
        return self.optimum - self.food.compute_values_fitness()
    
    def __z_max_value( self ):
        return 65*self.food.x[0] + 90*self.food.x[1] + 40*self.food.x[2] + 60*self.food.x[3] + 20*self.food.x[4]
    
    def __z_min_value( self ):
        return 150*self.food.x[0] + 300*self.food.x[1] + 40*self.food.x[2] + 100*self.food.x[3] + 10*self.food.x[4]
    
    def __search_best( self ):
        for index, salp in enumerate(self.swarm):
            if ( salp.is_better_than(self.food) ):
                self.food.copy(salp)

    def __init_rand( self ):
        s = None
        self.food = Salp()

        for i in range( 0, self.ps ):
            s = Salp()
            while( True ):
                if( s.is_feasible() ):
                    break
                s.fill_x_array()
            self.swarm.append(s)
        
        self.food.copy(self.swarm[0])

        self.__search_best()

        print(f"t: 0 - optimal value: {self.optimum} - compute fitness multi-objective function: {self.food.compute_values_fitness()} - difference: {self.__difference()} - rpd: {self.__rpd()}%\nz max value (exposition): {self.__z_max_value()}pts - z min value (costs): {self.__z_min_value()}[um] - best agent values: {self.food.x}\n")

    def __evolve( self ):
        for time in range(1, self.MaxIter + 1):
            s = Salp( apply_local_consistency = False )
            c1 = 2*math.pow( math.e, -math.pow( (4.0*time)/self.MaxIter, 2 ))
            for i in range(0, self.ps):
                while( True ):
                    s.copy(self.swarm[i])
                    if ( not i ):
                        s.leader_move(self.food, c1)
                    else:
                        s.follower_move(self.swarm[i - 1])
                    
                    if ( s.is_feasible() ):
                        break
 
                if ( s.is_better_than(self.swarm[i]) ):
                    self.swarm[i].copy(s)

            self.__search_best()

            print(f"t: {time} - optimal value: {self.optimum} - compute fitness multi-objective function: {self.food.compute_values_fitness()} - difference: {self.__difference()} - rpd: {self.__rpd()}%\nz max value (exposition): {self.__z_max_value()}pts - z min value (costs): {self.__z_min_value()}[um] - best agent values: {self.food.x}\n")
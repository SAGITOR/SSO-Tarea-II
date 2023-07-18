from Particle import Particle

class Swarm:

    def __init__( self ):
        self.ps = 25
        self.beta = 2
        self.g = None
        self.alpha = 2
        self.swarm = []
        self.theta = 0.9
        self.bestPoint = 0
        self.MaxIter = 200
        self.optimum = 0.676286850565496

    def execute( self ):
        self.__init_rand()
        self.__evolve()

    def __rpd( self ):
        return round(self.__difference() / self.optimum * 100, 2)
    
    def __difference( self ):
        return  self.optimum - self.g.compute_values_fitness()
    
    def __search_best( self ):
        for index, particle in enumerate(self.swarm):
            if ( particle.is_better_than(self.g) ):
                self.g.copy(particle)

    def __init_rand( self ):
        p = None
        self.g = Particle()

        for i in range( 0, self.ps ):
            p = Particle()
            while( True ):
                if( p.is_feasible() ):
                    break
                p.fill_x_array()
            self.swarm.append(p)
        
        self.g.copy(self.swarm[0])

        self.__search_best()

        print(f"t: {0} - optimal value: {self.optimum} - compute fitness: {self.g.compute_values_fitness()} - difference: {self.__difference()} - rpd: {self.__rpd()}% - best agent values: {self.g.p}\n")

    def __evolve( self ):
        for time in range(1, self.MaxIter + 1):
            p = Particle(apply_local_consistency = False)
            for i in range(0, self.ps):
                while( True ):
                    p.copy(self.swarm[i])
                    p.move( self.g, self.theta, self.alpha, self.beta )
                    if ( p.is_feasible() ):
                        break
 
                if ( p.is_better_than_p_best() ):
                    p.update_p_best()

                self.swarm[i].copy(p)

            self.__search_best()

            print(f"t: {time} - optimal value: {self.optimum} - compute fitness: {self.g.compute_values_fitness()} - difference: {self.__difference()} - rpd: {self.__rpd()}% - best agent values: {self.g.p}\n")
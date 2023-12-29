import pandas as pd
from pulp import *
import numpy as np

class Allocation:
    def __init__(self, m, n, p, matrix, w=None):
        self.matrix = matrix.copy()
        self.m = m
        self.n = n
        self.w = w
        self.p = p
        
    def solver(self):
        self._define_problem()
        self._decision_variable()
        self._objective_function()
        self._constraints()    
        
        # Solve the problem using branch-and-bound algorithm
        print(self.prob.solve(PULP_CBC_CMD(gapRel=0.0, threads=1, timeLimit=600)))
        
        
    def _define_problem(self):
        self.prob = LpProblem("p-median", LpMinimize)
    
    def _decision_variable(self):
        self.x = LpVariable.dicts("x", [(i,j) for i in range(self.m) for j in range(self.n)], 0, 1, LpBinary)
        self.y = LpVariable.dicts("y", [j for j in range(self.n)], 0, 1, LpBinary)
    
    def _objective_function(self):
        c = self.matrix.values
        w = self.w if self.w else [1 for w in range(self.m)]

        self.prob += lpSum([c[i][j] * self.x[(i,j)] * w[i] for i in range(self.m) for j in range(self.n)])
     
    def _constraints(self):   
        for i in range(self.m):
            self.prob += lpSum([self.x[(i,j)] for j in range(self.n)]) == 1

        for i in range(self.m):
            for j in range(self.n):
                self.prob += self.x[(i,j)] <= self.y[j]
                        
        self.prob += lpSum([self.y[j] for j in range(self.n)]) == self.p
        
    def get_result(self):
        df_matrix = self.matrix
        location = df_matrix.columns.values
        clients = df_matrix.index.values
        
        facilities = []
        X = np.zeros([self.m,self.n])
        times = []
        print("Optimal objective value:", value(self.prob.objective))
        for j in range(self.n):
            if self.y[j].value() > 0.5:
                facilities.append(location[j])
                print("Facility", j, "is located.", location[j])
                for i in range(self.m):
                    if self.x[(i,j)].value() > 0.5:
                        X[i,j]=1
                        times.append(df_matrix.iloc[i,j])
                        print("- Customer", i, "is served.", clients[i])
                        
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                if X[i,j] == 0:
                    df_matrix.iloc[i,j] = X[i,j]
        
        
        return facilities, times, df_matrix
        
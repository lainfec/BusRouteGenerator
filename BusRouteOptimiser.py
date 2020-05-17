import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import random
import Data_Transfer
import csv

fit=[0,0]
class RouteOptimizer:
    
    def __init__(self):
        self.bus_stops=None
        self.fleet_size=None
        self.link_data=None
        self.demand_matrix=None
        self.cur_population=None
        self.max_route_size=None
        self.generation_count=None
        self.starting_population=None
        self.shortest_time_matrix=None
        self.mut_prob=None
        self.copy_count=None
        
        
    def initialization(self):
        
        #making a list of tuples for activity of each bus stop
        activity_level=[[0,x] for x in range(len(self.bus_stops))]
        for x in range(len(self.bus_stops)):
            for i in range(len(self.bus_stops)):
                if i != x:
                    activity_level[x][0]+=self.demand_matrix[i][x]+self.demand_matrix[x][i]
        activity_level.sort()
        
        starting_population_size=self.starting_population
        self.cur_population=[[] for x in range(starting_population_size)]
        hyper_param_1=min(15,self.fleet_size)
        
        INS=activity_level[-(hyper_param_1):]
        probablity=[0 for x in range(len(INS))]
        sum=0
        for x in range(len(INS)):
            sum+=INS[x][0]
        for x in range(len(INS)):
            probablity[x]=INS[x][0]/sum
            
        INS_1D=[INS[x][1] for x in range(len(INS))]
        
        for x in range(starting_population_size):
            cur_route_set=[[] for i in range(self.fleet_size)]
            probablity_copy=[x for x in probablity]
            sum_copy=sum
            for i in range(self.fleet_size):
                    cur_choice=np.random.choice(INS_1D,1,p=probablity_copy)
                    cur_route_set[i].append(int(cur_choice))
                    indx=INS_1D.index(cur_choice)
                    sum_copy-=INS[indx][0]
                    probablity_copy[indx]=0
                    for y in range(len(INS)):
                        if probablity_copy[y]!=0:
                            probablity_copy[y]=INS[y][0]/sum_copy
                    if (i+1)%len(INS)==0:
                        probablity_copy=[x for x in probablity]
                        sum_copy=sum

            for i in range(self.fleet_size):
                cur_route_size=random.randint(math.floor(self.max_route_size*(3/4)),self.max_route_size)
                for y in range(1,cur_route_size):
                    temp_activity_level=[[0,z] for z in range(len(self.bus_stops))]
                    for z in range(len(self.bus_stops)):
                        for k in range(len(self.bus_stops)):
                                if z != k and z not in cur_route_set[i]:
                                    temp_activity_level[z][0]+=self.demand_matrix[k][z]+self.demand_matrix[z][k]

                    temp_activity_level.sort()
                    VNS=temp_activity_level[-(hyper_param_1):]
                    temp_probablity=[0 for z in range(len(VNS))]
                    sum_vns=0
                    for z in range(len(VNS)):
                        sum_vns+=VNS[z][0]
                    if sum_vns==0:
                        for z in range(len(self.bus_stops)):
                            for k in range(len(self.bus_stops)):
                                if z != k:
                                    temp_activity_level[z][0]+=self.demand_matrix[k][z]+self.demand_matrix[z][k]
                        
                        temp_activity_level.sort()
                        VNS=temp_activity_level[-(hyper_param_1):]
                        temp_probablity=[0 for z in range(len(VNS))]
                        sum_vns=0
                        for z in range(len(VNS)):
                            sum_vns+=VNS[z][0]
                    for z in range(len(VNS)):
                        temp_probablity[z]=VNS[z][0]/sum_vns
                    VNS_1D=[VNS[y][1] for y in range(len(VNS))]
                    cur_choice=np.random.choice(VNS_1D,1,p=temp_probablity)
                    cur_route_set[i].append(int(cur_choice))
                    
                        
            self.cur_population[x]=cur_route_set
            
            
            m=len(self.demand_matrix)
            self.shortest_time_matrix=[0 for x in range(m)]
            for i in range(m):
                k=i
                cost=[[0 for x in range(m)] for x in range(1)]
                offsets = []
                offsets.append(k)
                elepos=0
                for j in range(m):
                    cost[0][j]=self.link_data[k][j]
                mini=999
                for x in range (m-1):
                    mini=999
                    for j in range (m):
                            if cost[0][j]<=mini and j not in offsets:
                                    mini=cost[0][j]
                                    elepos=j
                    offsets.append(elepos)
                    for j in range (m):
                        if cost[0][j] >cost[0][elepos]+self.link_data[elepos][j]:
                            cost[0][j]=cost[0][elepos]+self.link_data[elepos][j]
                self.shortest_time_matrix[i]=cost
                
        
                    
                    
    def evaluation(self,route_set,store=0):
        
        tot_fit=0
        l=len(route_set)
        
        demand_ful=0
        tot_demand=0
        
        #calculating number of people who fulfilled their transport need
        n=len(self.demand_matrix)
        for x in range(n):
            for y in range(n):
                tot_demand+=self.demand_matrix[x][y]
                if self.demand_matrix[x][y] == 0 or x==y:
                    continue
                else:
                    for z in range(l):
                        route_len=len(route_set[z])
                        start_indx=[i for i in range(route_len) if route_set[z][i]==x]
                        end_indx=[i for i in range(route_len) if route_set[z][i]==y]
                        
                        if len(start_indx)==0 or len(end_indx)==0:
                            continue
                        elif start_indx[0]<end_indx[0]:
                            demand_ful+=self.demand_matrix[x][y]
                            
        tot_fit+=(demand_ful/tot_demand)*37              
        if store==1:
            fit[0]=(demand_ful/tot_demand)*100
        #calculating time fitness
        tot_time=0
        for x in range(n):
            for y in range(n):
                if self.demand_matrix[x][y]==0 or x==y:
                    continue
                min_time=100000
                for z in range(l):
                    cur_min_time=0
                    route_len=len(route_set[z])
                    if route_len==0:
                        continue
                    start_indx=[i for i in range(route_len) if route_set[z][i]==x]
                    end_indx=[i for i in range(route_len) if route_set[z][i]==y]
                    if len(start_indx)==0 or len(end_indx)==0:
                            continue
                    else:
                        for i in range(start_indx[0],end_indx[0]):
                            cur_min_time+=self.link_data[i][i+1]
                        if cur_min_time<min_time and cur_min_time!=0:
                            min_time=cur_min_time
                    
                if min_time != 100000:
                    tot_time+=(10-abs(self.shortest_time_matrix[x][0][y]-min_time)/self.shortest_time_matrix[x][0][y])
        tot_fit+=tot_time    
        if store==1:
            fit[1]=tot_time
                
        if store==0:
            return tot_fit
        else:
            return fit
        
    def modify(self):
        l=len(self.cur_population)
        #inter route crossover
        for x in range(l):
            cointoss=random.randint(0,1)
            if cointoss:
                second_string_indx=random.randint(0,l-1)
                if(len(self.cur_population[x])-1<=0 or len(self.cur_population[second_string_indx])-1<=0):
                    continue
                first_string_site=random.randint(0,len(self.cur_population[x])-1)
                second_string_site=random.randint(0,len(self.cur_population[second_string_indx])-1)
                self.cur_population[x][first_string_site],self.cur_population[second_string_indx][second_string_site]=self.cur_population[second_string_indx][second_string_site],self.cur_population[x][first_string_site]
                
                
        
        
        #intra route crossover
        copy_count=self.copy_count
        for x in range(l):
            for i in range(copy_count-1):
                self.cur_population+=[self.cur_population[i]]
        
        for x in range(l*copy_count):
            if(len(self.cur_population[x])-1<=0):
                continue
            first_string_indx=random.randint(0,len(self.cur_population[x])-1)
            second_string_indx=random.randint(0,len(self.cur_population[x])-1)
            min_len=min(len(self.cur_population[x][first_string_indx]),len(self.cur_population[x][second_string_indx]))
            min_len=random.randint(1,math.floor(min_len*4/5))
            temp_string=[self.cur_population[x][first_string_indx][i] for i in range(len(self.cur_population[x][first_string_indx]))]
            for y in range(min_len):
                self.cur_population[x][first_string_indx][y]=self.cur_population[x][second_string_indx][y]
                self.cur_population[x][second_string_indx][y]=temp_string[y]


        
        #reproduction
        fitness_ranking=[[self.evaluation(self.cur_population[x]),x] for x in range(l*copy_count)]
        tot_fit=0
        for x in range(l*copy_count):
            tot_fit+=fitness_ranking[x][0]
        probability=[0 for x in range(l*copy_count)]
        for x in range(l*copy_count):
            probability[x]=fitness_ranking[x][0]/tot_fit
        
        temp_population=[[] for x in range(l)]
    
        for x in range(l):
            cur_choice=np.random.choice(l*copy_count,1,p=probability)
            tot_fit-=fitness_ranking[int(cur_choice)][0]
            probability[int(cur_choice)]=0
            for y in range(l*copy_count):
                    if probability[y]!=0:
                        probability[y]=fitness_ranking[y][0]/tot_fit
            temp_population[x]=self.cur_population[int(cur_choice)]
        
        #Mutation 
        for x in range(l):
            y=random.random()
            if y<self.mut_prob:
                i=random.randint(0,len(temp_population[x])-1)
                indx1=random.randint(0,len(temp_population[x][i])-1)
                indx2=random.randint(0,len(temp_population[x][i])-1)
                temp_population[x][i][indx1],temp_population[x][i][indx2]=temp_population[x][i][indx2],temp_population[x][i][indx1]
        self.cur_population=temp_population
        
        
    def optimize(self):
        self.initialization()
        
        max_fit_x,avg_fit_x=[],[]
        for g in range(self.generation_count):
            self.modify()
            fitness_ranking=[self.evaluation(self.cur_population[i]) for i in range(len(self.cur_population))]
            max_fit=-1
            indx=-1
            avg_fitness=0
            for x in range(len(self.cur_population)):
                if max_fit<fitness_ranking[x]:
                    max_fit,indx=fitness_ranking[x],x
                avg_fitness+=fitness_ranking[x]
            max_fit_x.append(max_fit)
            avg_fit_x.append(avg_fitness/len(self.cur_population))
            
            
        return self.cur_population,max_fit_x,avg_fit_x
    

def model_run(data):
    fleet_size,bus_stop_data,demand_matrix,link_matrix=Data_Transfer.data_transfer()
    GA=RouteOptimizer()
    GA.max_route_size=data[3]
    GA.generation_count=data[0]
    GA.starting_population=data[1]
    GA.fleet_size=fleet_size
    GA.bus_stops=bus_stop_data
    GA.demand_matrix=demand_matrix
    GA.link_data=link_matrix
    GA.mut_prob=data[2]/100
    GA.copy_count=data[4]
    GA.initialization()
    final_pop,max_fit_x,avg_fit_x=GA.optimize()
    fitness_ranking=[GA.evaluation(final_pop[i]) for i in range(len(final_pop))]
    indx=-1
    max_fit=-1
    for x in range(len(final_pop)):
        if max_fit<fitness_ranking[x]:
            max_fit,indx=fitness_ranking[x],x
    
    with open('route_set_generated.csv','w',newline='') as csvfile:
        writer=csv.writer(csvfile)
        writer.writerow(['Route_No','Route_Detail'])
        for x in range(len(final_pop[indx])):
            route_string=''
            for y in range(len(final_pop[indx][x])-1):
                route_string+=str(bus_stop_data[final_pop[indx][x][y]][1])+', '
            route_string+=str(bus_stop_data[final_pop[indx][x][len(final_pop[indx][x])-1]][1])
            writer.writerow([x+1,route_string])

    last_fit= GA.evaluation(final_pop[indx],1)
   
    return final_pop[indx],max_fit_x,avg_fit_x,last_fit[0],last_fit[1]

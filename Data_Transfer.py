import pandas as pd
import numpy as np


def data_transfer():
    demand_matrix_df=pd.read_csv("bus_dataset/Demand_Matrix.csv")
    bus_stop_data_df=pd.read_csv("bus_dataset/Bus_Stop_Data.csv")
    fleet_data=pd.read_csv("bus_dataset/Fleet_Data.csv")
    time_data_df=pd.read_csv("bus_dataset/Link_Travel_Time.csv")
    
    num_bus_stops=len(bus_stop_data_df.index)
    num_buses=len(fleet_data.index)
    
    demand_matrix=[]
    link_matrix=[]
    bus_stop_data=[]
    for x in range(num_bus_stops):
        cur_demand=[]
        cur_link=[]
        for y in range(num_bus_stops):
            if x==y:
                cur_demand.append(0)
                cur_link.append(0)
            else:
                cur_demand.append(demand_matrix_df.iloc[x*num_bus_stops+y][2])
                cur_link.append(time_data_df.iloc[x*num_bus_stops+y][2])
        bus_stop_data.append([bus_stop_data_df.iloc[x][0],bus_stop_data_df.iloc[x][1]])
        demand_matrix.append(cur_demand)
        link_matrix.append(cur_link)
        
    return num_buses, bus_stop_data,demand_matrix,link_matrix


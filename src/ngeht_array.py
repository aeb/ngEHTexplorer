import numpy as np


def read_array(array_file_name,existing_station_list=None) :

    if (existing_station_list is None) :
        existing_station_list = ['PV','AZ','SM','LM','AA','AP','SP','JC','GL','PB','KP','HA']
    
    stations = np.loadtxt(array_file_name,usecols=[0],dtype=str)
    locs = np.loadtxt(array_file_name,usecols=[1,2,3])
    sefd = np.loadtxt(array_file_name,usecols=[4,5,6,7,8])
    cost_factors = np.loadtxt(array_file_name,usecols=[9,10,11])
    sefd_freq = np.array([86,230,345,480,690])
    
    statdict = {}
    for j in range(len(stations)) :
        if (stations[j] in existing_station_list) :
            statdict[stations[j]] = {'on':True,'loc':locs[j],'sefd':sefd[j],'sefd_freq':sefd_freq,'name':stations[j],'exists':True,'diameter':None,'cost_factors':cost_factors[j]}
        else :
            statdict[stations[j]] = {'on':True,'loc':locs[j],'sefd':sefd[j],'sefd_freq':sefd_freq,'name':stations[j],'exists':False,'diameter':6,'cost_factors':cost_factors[j]}

    return statdict



def cost_model(statdict,ngeht_diameter,opex_exclude=None) :

    # Semi-autonomous
    total_new_site_NRE = 2.655 * 2 * (ngeht_diameter/3.5)**0.67  # Approximate diameter dependence that matches to 4%

    if (opex_exclude is None) :
        opex_exclude = []
        
    capex = total_new_site_NRE
    # print("tota_new_site_NRE %10.5g"%(capex))
    opex = 0.0
    for s in statdict.keys() :
        if (statdict[s]['on'] and (not s in opex_exclude)) :
            capex = capex + statdict[s]['cost_factors'][0] + statdict[s]['cost_factors'][1]*ngeht_diameter**2.7
            # opex = opex + 0.139726 + statdict[s]['cost_factors'][2]
            opex = opex + statdict[s]['cost_factors'][2]
            # print("%2s %10.4g %10.4g %10.4g"%(s,capex,statdict[s]['cost_factors'][0] + statdict[s]['cost_factors'][1]*ngeht_diameter**2.7,statdict[s]['cost_factors'][2]))
    # print("capex,opex:",capex,opex)
    #print("%5.1f"%(opex))
    return capex,opex
            


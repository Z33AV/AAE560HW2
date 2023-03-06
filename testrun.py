import mesa
import uam_model
import matplotlib.pyplot as plt




# NOTE: This is the main file to run the sims
if __name__ == "__main__":
    numVehicles_totalmax = 10000 #maximum number of allowable vehicles, will never actually be this number due to random generator
    max_V = 100 # NOTE: raise of lower to control number of ports - > better to have many or few?
    num_ports = int(numVehicles_totalmax/max_V) # NOTE: number of vertiports

    Vehicle_MaxRange = 9 #ranges from 0 to 9
    VOE = 1.0 # NOTE: vehicle operating energy constant, inverse efficiency metric of vehicle, lower is better.
    # NOTE: instantiate the simulation
    sim = uam_model.UAMModel(num_ports,Vehicle_MaxRange, max_V, VOE)
    totVec = []
    # NOTE: Running the simulation
    i_list = []
    for i in range(1000):
        sim.step()
        s = 0
        for ag in sim.schedule.agents:
            s += ag.nV
        totVec.append(s)
        i_list.append(i)
        print(i)

    AgentIds = []
    ConsumedEnergy = []
    for agent in sim.schedule.agents:
        AgentIds.append(agent.uid)
        ConsumedEnergy.append(abs(agent.E))

    EperPort_avg = sum(ConsumedEnergy)/num_ports
    print(EperPort_avg)


    plt.figure(1)
    plt.bar(AgentIds, ConsumedEnergy, width = 1, align = 'center')

    plt.savefig("Bar plot of Total Consumed Energy per VertiPort")


    plt.figure(2)
    plt.plot(i_list, totVec)
    plt.savefig("total vehicles in sim vs time")

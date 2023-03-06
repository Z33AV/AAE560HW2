import mesa
import uam_model
import matplotlib.pyplot as plt
from numpy import linspace

# NOTE: This is the main file to run the sims
if __name__ == "__main__":
    # NOTE: define constants for this batch run of the sims

    numVehicles_totalmax = 10000 #maximum number of allowable vehicles, will never actually be this number due to random generator
    Vehicle_MaxRange = 9 #ranges from 0 to 9
    VOE = 1.0 # NOTE: vehicle operating energy constant, inverse efficiency metric of vehicle, lower is better.
    numDataPoints = 1000
    t = 1000
    #Define batch run variable parameter
    max_Vs = list(range(10, 75))
    print(max_Vs)
    num_ports = []
    for K in max_Vs:
        num_ports.append(int(numVehicles_totalmax/K))
    print(num_ports)
    EperPort_avg = []

    for j in range(0,len(max_Vs)):
        print(j)
        sim = uam_model.UAMModel(num_ports[j],Vehicle_MaxRange, max_Vs[j], VOE)

        for i in range(0,t):
            sim.step()
            print("sim step" + str(i))

        totE = 0
        EperPort = 0
        for ag in sim.schedule.agents:
            totE += abs(ag.E)

        EperPort = totE/num_ports[j]
        EperPort_avg.append(EperPort)



    plt.figure(1)
    plt.scatter(num_ports, EperPort_avg)


    plt.xlabel("Number of Vertiports")
    plt.ylabel("Average Energy Consumption per VertiPort")
    plt.title("Sensitivity of AEC per VertiPort vs. Number of VertiPorts")
    plt.savefig("ReRun Sensitivity of AEC per VertiPort vs. Number of VertiPorts.jpg")

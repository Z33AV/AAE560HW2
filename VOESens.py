import mesa
import uam_model
import matplotlib.pyplot as plt
from numpy import linspace

# NOTE: This is the main file to run the sims
if __name__ == "__main__":
    # NOTE: define constants for this batch run of the sims
    max_V = 25
    numVehicles_totalmax = 10000 #maximum number of allowable vehicles, will never actually be this number due to random generator
    Vehicle_MaxRange = 9 #ranges from 0 to 9
     # NOTE: vehicle operating energy constant, inverse efficiency metric of vehicle, lower is better.
    numDataPoints = 1000
    t = 1000
    num_ports=int(numVehicles_totalmax/max_V)



    #Define batch run variable parameter
    VOE = linspace(0.1,1,numDataPoints)
    print(VOE)
    efficiency = []
    for K in VOE:
        efficiency.append(1-K)
    print(efficiency)
    EperPort_avg = []

    for j in range(0,len(VOE)):
        print(j)
        sim = uam_model.UAMModel(num_ports,Vehicle_MaxRange, max_V, VOE[j])

        for i in range(0,t):
            sim.step()
            print("sim step" + str(i))

        totE = 0
        EperPort = 0
        for ag in sim.schedule.agents:
            totE += abs(ag.E)

        EperPort = totE/num_ports
        EperPort_avg.append(EperPort)



    plt.figure(1)
    plt.scatter(efficiency, EperPort_avg)


    plt.xlabel("Vehicle Efficiency")
    plt.ylabel("Average Energy Consumption per VertiPort")
    plt.title("Sensitivity of AEC per VertiPort vs. Vehicle Efficiency")
    plt.savefig("Sensitivity of AEC per VertiPort vs. Vehicle Efficiency.jpg")

import mesa
import uam_model
import matplotlib.pyplot as plt
from numpy import linspace

# NOTE: This is the main file to run the sims
if __name__ == "__main__":
    # NOTE: define constants for this batch run of the sims
    max_V = 25
    numVehicles_totalmax = 10000 #maximum number of allowable vehicles, will never actually be this number due to random generator
    VOE = 1.0 #ranges from 0 to 9
     # NOTE: vehicle operating energy constant, inverse efficiency metric of vehicle, lower is better.
    numDataPoints = 1000
    t = 1000
    num_ports=int(numVehicles_totalmax/max_V)



    #Define batch run variable parameter
    Vehicle_MaxRange = list(range(1,19))

# NOTE: Holdovers from previous code
    #print(VOE)
    #efficiency = []
    #for K in VOE:
    #    efficiency.append(1-K)
    #print(efficiency)
# NOTE: Resume actual code

    EperPort_avg = []

    for j in range(0,len(Vehicle_MaxRange)):
        print(j)
        sim = uam_model.UAMModel(num_ports,Vehicle_MaxRange[j], max_V, VOE)

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
    plt.scatter(Vehicle_MaxRange, EperPort_avg)


    plt.xlabel("Vehicle Maximum Range")
    plt.ylabel("Average Energy Consumption per VertiPort")
    plt.title("Sensitivity of AEC per VertiPort vs. Vehicle Max Range (Extended)")
    plt.savefig("ReRun Sensitivity of AEC per VertiPort vs. Vehicle Max Range.jpg")

#UAM ABM for Energy Consumption - Ziyan Virani HW2

import mesa
import random as rand
import math



class VertiPort(mesa.Agent):
    #Agent with given initial properties

    def __init__(self, uid, model, numVehicles, E, asid):
        # NOTE: Define properties of VertiPort here
        super().__init__(uid, model)
        self.nV = numVehicles
        #self.pos = pos
        self.E = E
        self.uid = uid
        self.airspace_id = asid
        self.has_objective = 0
        self.target_port = None
        #print("VertiPort " + str(self.uid) +" init with properties Energy = "+ str(self.E) + ", Airspace = "+str(self.airspace_id)+", numVehicles = " +
        #    str(self.nV)+'\n')


    def step(self):
        #agent step function
        #print("Agent " + str(self.uid) +" step")
        self.E -= 0.5 #overhead operating energy of the port itself
        N = rand.randint(0,self.nV)
        self.ChosenSendVehicles(N)
        #print("VertiPort " + str(self.uid) +" stepped, new properties Energy = "+ str(self.E) + ", Airspace = "+str(self.airspace_id)+", numVehicles = " +
        #    str(self.nV)+"objective status: "+str(self.has_objective)+'\n') # NOTE: for use with unit tests in Agtest.py

    def choosePort(self):
        for i in range(0,len(self.model.schedule.agents)):
            Vport = self.random.choice(self.model.schedule.agents)
            if abs(Vport.airspace_id - self.airspace_id) >= self.model.Vehicle_MaxRange:
                continue
            else:
                #print("destination chosen") # NOTE: to be used with Agtest
                return Vport

    def ChosenSendVehicles(self, N):
        Ntemp = 0
        # NOTE: Determine if the objective from the last turn was cleared, if not, priority goes to moving those vehicles to the port they need to reach.
        if not (self.has_objective):
            Vport = self.choosePort() #chooses destination that respects vehicle range limitation
            self.target_port = Vport
            self.has_objective = 1
        #    print("New objective generated") # NOTE: for use with unit tests in Agtest.py
        else:
            Vport = self.target_port
        #    print("exisitng objective recycled") # NOTE: for use with unit tests in Agtest.py

        if (Vport.nV + N > self.model.max_V):
             # NOTE: one weird consequence of this line: sometimes one node will connect with a full node, and chose to not send any vehicles
            Ntemp = self.model.max_V - Vport.nV
            self.E -= (abs(self.airspace_id - Vport.airspace_id) + 2)*self.model.VOE*Ntemp
            self.nV = self.nV - Ntemp
        #    print("Vport " + str(self.uid) + " sent " + str(Ntemp)+" vehicles to Vport "+str(Vport.uid) +"\n") # NOTE: for use with unit tests in Agtest.py
            Vport.ReceiveVehicles(Ntemp)

        elif(Vport.nV + N <= self.model.max_V):
            self.E -= (abs(self.airspace_id - Vport.airspace_id) + 2)*self.model.VOE*N
            self.nV = self.nV - N
        #    print("Vport " + str(self.uid) + " sent " + str(N)+" vehicles to Vport "+str(Vport.uid) +"\n")# NOTE: for use with unit tests in Agtest.py
            Vport.ReceiveVehicles(N)

            self.has_objective = 0
        #    print("objective cleared")# NOTE: for use with unit tests in Agtest.py

    def RandSendVehicles(self, N):
        # NOTE: choose another VertiPort
        Vport = self.random.choice(self.model.schedule.agents)
        # NOTE: sends vehicles to another VertiPort. If nodes are closer, energy expenditure per vehicle is lower.
        if (Vport.nV + N > self.model.max_V): # NOTE: one weird consequence of this line: sometimes one node will connect with a full node, and chose to not send any vehicles
            N = self.model.max_V - Vport.nV
            self.E -= (abs(self.airspace_id - Vport.airspace_id) + 1)*self.model.VOE*N
            self.nV = self.nV - N
            #print("Vport " + str(self.uid) + " sent " + str(N)+" vehicles to Vport "+str(Vport.uid) +"\n")
            Vport.ReceiveVehicles(N)



    def ReceiveVehicles(self, N):  # NOTE: NEVER call this in class or in-situ, as it is called only by the send function. If done, double count
        self.nV = self.nV + N
        #print("Vport " + str(self.uid) + " received " + str(N)+" vehicles, and now has "+ str(self.nV) +" vehicles \n")



class UAMModel(mesa.Model):
    #model with agents, to be run (executable)

    def __init__(self, N, vmr, max_V, VOE):
        self.Vehicle_MaxRange = vmr
        self.max_V = max_V
        self.numAgs = N
        self.VOE = VOE
        self.schedule = mesa.time.RandomActivation(self) # NOTE: to use random or simultaneous?
        # NOTE: instantiate agents now
        for i in range(self.numAgs):
            numVehicles = rand.randint(0,self.max_V)
            E = 0 # NOTE: all agents start with 0 energy because we are measuring usage/change; actual energy state is irrelevant
            asid = rand.randint(1,20)
            #asid = 1 # NOTE: TEST CASE
            a = VertiPort(i,self, numVehicles, E, asid)

            self.schedule.add(a)

    def step(self):
        self.schedule.step() # NOTE: Steps the whole model

# NOTE: Unit tests for the Veritport Agent

import mesa

from uam_model import *

test = UAMModel(25,2,5,1)

if test.schedule.get_agent_count() == 25:
    print("model init test passed \n")
else:
    print("Model init test failed, agent count discrepancy \n")

test.step()


#print(test.schedule.agents)

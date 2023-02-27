from communication import talk
from simulator import Simulator
from config import test_conf, prod_conf
# talk()

sim = Simulator(test_conf)
sim.run()

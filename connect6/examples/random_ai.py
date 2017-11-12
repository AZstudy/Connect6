from connect6 import AIAbstractClass
import random
import time

class RandomAI(AIAbstractClass):
    def action(self,states):
        return (random.randint(0, 8), random.randint(0, 8))

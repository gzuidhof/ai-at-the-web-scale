import numpy as np
from models import *

class BootstrapThompsonSampler(Model):

    def __init__(self):
        self.models = [LinearModel() for _ in range(1000)]


    def propose(self, context):
        return np.random.choice(self.models).propose(context)

    def observe(self, context, action, reward):
        #super(BootstrapThompsonSampler, self).observe(context, action, reward)

        for model in self.models:
            if np.random.rand(1) > 0.5:
                model.observe(context, action, reward)

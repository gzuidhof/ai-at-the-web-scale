import numpy as np
from models import *

class BootstrapThompsonSampler(Model):

    def __init__(self, n_models = 1000, modelType = LinearModel):
        self.models = [modelType() for _ in range(n_models)]

    def propose(self, context):
        return np.random.choice(self.models).propose(context)

    def observe(self, context, action, reward):
        # Super class prints some information.
        super(BootstrapThompsonSampler, self).observe(context, action, reward)

        for model in self.models:
            if np.random.rand(1) > 0.5:
                model.observe(context, action, reward)

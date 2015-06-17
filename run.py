from context_get_pool import ContextGetPool
import api
import random_model
import itertools

class ModelRunner():
    """
        Runner of a model, collects contexts and tracks performance

        Constructor takes two arguments
            act: function(context): action
            "Ask the model to make a choice"

            observe: function(context, action, reward): None
            "Model observes reward of previous action"
    """

    def __init__(self, act, observe):
        self.act = act
        self.observe = observe

    def run(self, run_ids = [0], ids = range(100)):

        getter = ContextGetPool()

        context_ids = [c for c in itertools.product(run_ids, ids)]
        context_gen = getter.get(context_ids)


        for (id, run_id), context in itertools.izip(context_ids, context_gen):
            action = self.act(context)
            reward = api.propose_page(id, run_id, action)
            self.observe(context, action, reward)


if __name__ == '__main__':

    #Simply prints the observation
    def print_observe(context, action, reward):
        print '--------'
        print 'Reward:',reward
        print 'Action:',action
        print 'Context:',context

    runner = ModelRunner(random_model.rand_proposal, print_observe)
    runner.run()

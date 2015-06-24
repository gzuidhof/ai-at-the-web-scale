from context_get_pool import ContextGetPool
import api
from bts import *
from models import *

import itertools
import numpy as np

class ModelRunner():
	"""
		Runner of a model, collects contexts and tracks performance

		Constructor takes two arguments
			act: function(context): action
			"Ask the model to make a choice"

			observe: function(context, action, reward): None
			"Model observes reward of previous action"
	"""

	def __init__(self, model):
		self.model = model

	def run(self, run_ids = [0], ids = [0]*100000):

		getter = ContextGetPool()

		context_ids = [c for c in itertools.product(run_ids, ids)]
		context_gen = getter.get(context_ids)

		rewards = []
		successes = []

		for (run_id, id), context in itertools.izip(context_ids, context_gen):
			#Perform an action
			action = self.model.propose(context)


			#Get the response, determine reward
			response = api.propose_page(id, run_id, action)
			success, reward = self.extract_reward(response, action)

			#Observe the reward
			self.model.observe(context, action, reward)

			#Collect some statistics
			rewards.append(reward)
			successes.append(success)
			print "Reward: %.2f, mean reward: %.2f, std reward: %.2f" % (reward, np.mean(rewards), np.std(rewards)), '(%.2f)'%action[-1]
			print "Success: %i, percent success: %.2f" % (success, np.mean(successes) * 100)

	def extract_reward(self, response, action):
		#0 or 1
		success = response['effect']['Success']

		#success * price
		reward = success * action[-1]

		return success, reward

if __name__ == '__main__':
	runner = ModelRunner(BootstrapThompsonSampler())
	runner.run()

from context_get_pool import ContextGetPool
import api
from bts import *
from models import *
import plotta

import itertools
import numpy as np

import matplotlib.pyplot as plt

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
		self.job = plotta.Job(type(model).__name__)

	def run(self, run_ids = [1], ids = range(10000)):

		getter = ContextGetPool()

		context_ids = [c for c in itertools.product(run_ids, ids)]
		context_gen = getter.get(context_ids)

		rewards = []
		successes = []
		mean_rewards = []

		self.job.start()
		mean_stream = self.job.add_stream('Mean reward')

		i = 0
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
			mean_rewards.append(np.mean(rewards))

			mean_stream.append(i, mean_rewards[-1])

			print "ID: %i, reward: %.2f, mean reward: %.2f, std reward: %.2f" % (id, reward, np.mean(rewards), np.std(rewards)), '(%.2f)'%action[-1]
			print "Success: %i, percent success: %.2f" % (success, np.mean(successes) * 100)
			i+=1

		plt.plot(ids, mean_rewards)
		plt.show()

	def extract_reward(self, response, action):
		#0 or 1
		success = response['effect']['Success']

		#success * price
		reward = success * action[-1]

		return success, reward

if __name__ == '__main__':
	runner = ModelRunner(ContextlessThompsonModel())
	runner.run()

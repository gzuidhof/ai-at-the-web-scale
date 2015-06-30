from context_get_pool import ContextGetPool
import api
from bts import *
from models import *
import plotta

import itertools
import numpy as np

import matplotlib.pyplot as plt
import time

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

	def run(self, run_ids = [4], ids = range(4000)):

		getter = ContextGetPool()

		context_ids = [c for c in itertools.product(run_ids, ids)]
		context_gen = getter.get(context_ids)

		rewards = []
		successes = []
		mean_rewards = []
		actions = []
		cum_reward = 0

		#self.job.start()
		#mean_stream = self.job.add_stream('Mean reward')
		#mean100_stream = self.job.add_stream('Mean reward100')
		#cum_stream = self.job.add_stream('Cumulative reward')


		start = time.time()
		print "Starting!"

		i = 0
		for (run_id, id), context in itertools.izip(context_ids, context_gen):
			#Perform an action
			action = self.model.propose(context)

			#Get the response, determine reward
			response = api.propose_page(id, run_id, action)
			success, reward = self.extract_reward(response, action)

			actions.append(action[-1])

			#Observe the reward
			self.model.observe(context, action, reward)

			#Collect some statistics
			rewards.append(reward)
			successes.append(success)
			mean_rewards.append(np.mean(rewards))
			cum_reward += reward

			#mean_stream.append(i, mean_rewards[-1])
			#mean100_stream.append(i, np.mean(rewards[-100:]))
			#cum_stream.append(i, cum_reward)


			#print "ID: %i, reward: %.2f, mean reward: %.2f, std reward: %.2f" % (id, reward, np.mean(rewards), np.std(rewards)), '(%.2f)'%action[-1]
			#print "Success: %i, percent success: %.2f" % (success, np.mean(successes) * 100)
			i+=1

		print "Cumulative reward:", cum_reward
		print "mean reward: %.2f, std reward: %.2f" % (np.mean(rewards), np.std(rewards))
		print "Running time:", time.time()-start, "---"

		return cum_reward, np.mean(rewards), np.std(rewards), time.time()-start

		#plt.scatter(ids, actions)
		#plt.show()

	def extract_reward(self, response, action):
		#0 or 1
		success = response['effect']['Success']

		#success * price
		reward = success * action[-1]

		return success, reward

if __name__ == '__main__':


	cum_rewards = []
	mean_rewards = []
	std_rewards = []
	times = []

	for run_id in range(0, 5000, 1000):
		print 'run_id:', run_id
		runner = ModelRunner(ContextlessThompsonModel())
		cr, m, std, timed = runner.run(run_ids=[run_id])
		cum_rewards.append(cr)
		mean_rewards.append(m)
		std_rewards.append(std)
		times.append(timed)

	print "MEAN CUM REWARD", sum(cum_rewards)/len(cum_rewards)
	print "MEAN AVG REWARD", sum(mean_rewards)/len(mean_rewards)
	print "MEAN STD REWARD", sum(std_rewards)/len(std_rewards)
	print "MEAN TIME", sum(times)/len(times)

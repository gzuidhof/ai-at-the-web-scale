from constants import *

import encode
import decode
import random
import time
import numpy as np
import util
from scipy.optimize import minimize
import os.path

import sklearn.linear_model


class Model(object):
	def propose(self, context):
		pass

	def observe(self, context, action, reward):
		print '--------'
		print 'Reward:',reward
		print 'Action:',action
		print 'Context:',context

class RandomModel(Model):
	#Override
	def propose(self, context):

		header = random.choice(HEADER_TYPES)
		adtype = random.choice(AD_TYPES)
		color = random.choice(COLOR_TYPES)
		product_id = random.choice(PRODUCT)
		price = random.uniform(PRICE_MIN, PRICE_MAX)

		return header, adtype, color, product_id, price

	def observe(self, context, action, reward):
		pass

class LinearModel(Model):

	def __init__(self, eta = 0.0001):

		num_context_variables = 1+ len(AGENTS)+len(REFERERS)+len(LANGUAGES)
		num_action_variables = 2 + len(COLOR_TYPES)+len(AD_TYPES)+len(HEADER_TYPES) + 1

		num_interactions = (num_context_variables + num_action_variables) * (num_context_variables + num_action_variables - 1) / 2

		num_weights = num_context_variables + num_action_variables + num_interactions

		self.weights = np.zeros((num_weights))
		self.bias = 0

		# Initialize previous actions array to have warm start when maximizing
		# In order: [price, productid, color, adtype, header]
		# where color is green, adtype is skyscraper and header is 15
		#self.prev_actions = np.array([5.00, 18, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0])
		self.prev_actions = np.array(encode.encode_action([15,'skyscraper','green',18,5.0]))

		self.num_context_variables = num_context_variables
		self.num_action_variables = num_action_variables

		self.eta = eta
		self.i = 0
		self.random = RandomModel()

		context_bounds = [(AGE_MIN, AGE_MAX)] + \
						[(0,1)]* (len(AGENTS)+len(REFERERS)+len(LANGUAGES))

		action_bounds = [(PRICE_MIN, PRICE_MAX), (PRODUCT_MIN, PRODUCT_MAX)] + \
		 				[(0,1)]* (len(COLOR_TYPES)+len(AD_TYPES)+len(HEADER_TYPES)) +\
						[(PRICE_MIN**2, PRICE_MAX**2)]

		self.bounds = context_bounds + action_bounds
		self.context_bounds = context_bounds
		self.action_bounds = action_bounds
		self.vectors = []
		self.rewards = []

		if os.path.isfile('weights.npy'):
			loaded_weights = np.load("weights.npy")
			if len(loaded_weights) == len(self.weights):
				self.weights = np.load("weights.npy")

	def _build_interactions(self, vector):
		interactions = []

		for i in range(0, len(vector)):
			for j in range(i+1, len(vector)):
				interactions.append(vector[i] * vector[j])

		return np.array(interactions)

	def _linear_function(self, actions, context):
		# Form: y = b_0 + b_1 * context[0] + b_2 * context[1] + ... + b_{n+1} * action[0] + b_{n+2} * action[1] + ...
		# Where y is the reward (to be maximized), b_0 through b_n are the context weights and b_{n+1} through b_{m-n} are the action weights

		# First, transform context to vector
		context_vector = encode.encode_context(context)

		# Create information vector by concatenating the context with the actions
		information_vector = np.concatenate((context_vector, actions))
		information_vector = np.concatenate((information_vector, [-actions[0]**2]))

		# Interactions
		information_vector = np.concatenate((information_vector, self._build_interactions(information_vector)))

		# Take inner product of weights and information_vector
		y = self.bias + np.inner(self.weights, information_vector)

		return y, information_vector

	def _linear_model(self, actions, context):
		y, _ = self._linear_function(actions, context)

		# Return negative since we want to maximize instead of minimize
		return -y

	# Override
	def propose(self, context):
		self.i += 1

		if self.i < 1000:
			print "EXPLORATION PHASE %i" % self.i
			return self.random.propose(context)

		print "EXPLOITATION PHASE %i" % self.i

		bounds = self.action_bounds[:-1]
		#print bounds

		# Use previous action weights as initialization to have a warm start
		result = minimize(self._linear_model, self.prev_actions, args = (context['context']), method = 'L-BFGS-B', bounds = bounds, options = {'maxiter': 1000})

		action = result['x']
		self.prev_actions = action

		return decode.decode_action(action)

	def observe(self, context, action, reward):
		# Print to screen in super method
		#super(LinearModel, self).observe(context, action, reward)

		action_vector = encode.encode_action(action)

		# Predicted reward
		fx, information_vector = self._linear_function(action_vector, context['context'])
		self.vectors.append(information_vector)
		self.rewards.append(reward)

		np.save("vectors.npy", np.array(self.vectors))
		np.save("rewards.npy", np.array(self.rewards))

		# SSE grad
		error = (reward - fx)

		#information_vector = np.array([v / float(x[1]) for v, x in zip(information_vector, self.bounds)])
		#information_vector = np.clip(information_vector, -1, 1)
		information_vector[0] /= 110.
		information_vector[12] /= 50.
		information_vector[13] = (information_vector[13] - 18) / 8.
		information_vector[-1] /= 50.**2

		# Update weights and bias
		self.weights += (self.eta / self.i**0.25) * error * information_vector - 0.01 * self.weights
		self.bias += (self.eta / self.i**0.25) * error

		# Print diagnostics
		print "Action: ", action
		print "Context: ", context
		print "Predicted reward: %.2f" % fx
		print "Error: %.2f" % error
		util.print_weights(self.bias, self.weights)


class ContextlessThompsonModel(Model):

	def __init__(self):
		self.price_bins = 5

		self.a = np.ones((len(HEADER_TYPES), len(AD_TYPES), len(COLOR_TYPES), self.price_bins, 5))
		self.b = np.ones((len(HEADER_TYPES), len(AD_TYPES), len(COLOR_TYPES), self.price_bins, 5))

	def arm_to_action(self, arm):
		return HEADER_TYPES[arm[0]], AD_TYPES[arm[1]], COLOR_TYPES[arm[2]], arm[4] + 10, (arm[3] + 1) * (50 / self.price_bins)

	def action_to_arm(self, action):
		return HEADER_TYPES.index(action[0]), AD_TYPES.index(action[1]), COLOR_TYPES.index(action[2]), action[4] / (50 / self.price_bins) - 1, action[3] - 10

	# Override
	def propose(self, context):
		it = np.nditer(self.a, flags=['multi_index'])

		samples = np.ones_like(self.a)

		while not it.finished:
			ix = it.multi_index
			samples[ix] = np.random.beta(self.a[ix], self.b[ix])
			it.iternext()

		best = np.argmax(samples)
		best = np.unravel_index(best, self.a.shape)

		return self.arm_to_action(best)

	# Override
	def observe(self, context, action, reward):
		super(ContextlessThompsonModel, self).observe(context, action, reward)

		arm = self.action_to_arm(action)

		if reward > 0:
			self.a[arm] += 1
		else:
			self.b[arm] += 1

		print np.unravel_index(np.argmax(self.a), self.a.shape)

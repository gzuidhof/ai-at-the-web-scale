from constants import *

import encode
import random
import time
import numpy as np
from scipy.optimize import minimize

from collections import OrderedDict

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

	def __init__(self, num_context_variables = 12, num_action_variables = 14, eta = 0.00001):
		num_interactions = (num_context_variables + num_action_variables) * (num_context_variables + num_action_variables - 1) / 2

		self.weights = np.zeros((num_context_variables + num_action_variables + num_interactions))
		#self.weights = np.random.rand(num_context_variables + num_action_variables + num_interactions)
		self.bias = 0

		# Initialize previous actions array to have warm start when maximizing
		# In order: [price, productid, color, adtype, header]
		# where color is green, adtype is skyscraper and header is 15
		self.prev_actions = np.array([5.00, 18, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0])

		self.num_context_variables = num_context_variables
		self.num_action_variables = num_action_variables

		self.eta = eta
		self.i = 0
		self.random = RandomModel()

		self.bounds = [(AGE_MIN, AGE_MAX), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (PRICE_MIN, PRICE_MAX), (PRODUCT_MIN, PRODUCT_MAX), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (PRICE_MIN**2, PRICE_MAX**2)]
		self.vectors = []
		self.rewards = []

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
		information_vector = np.concatenate((information_vector, [actions[0]**2]))

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

		if self.i < 1:
			print "EXPLORATION PHASE %i" % self.i
			return self.random.propose(context)

		print "EXPLOITATION PHASE %i" % self.i

		bounds = self.bounds[self.num_context_variables:-1]

		# Use previous action weights as initialization to have a warm start
		result = minimize(self._linear_model, self.prev_actions, args = (context['context']), method = 'L-BFGS-B', bounds = bounds, options = {'maxiter': 1000})

		action = result['x']
		self.prev_actions = action

		header = encode.one_hot_reverse('Header', action[10:13])
		ad_type = encode.one_hot_reverse('AdType', action[7:10])
		color = encode.one_hot_reverse('Color', action[2:7])

		product = np.clip(int(np.round(action[1])), PRODUCT_MIN, PRODUCT_MAX)
		price = np.clip(action[0], PRICE_MIN, PRICE_MAX)

		return header, ad_type, color, product, price

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
		information_vector = np.clip(information_vector, -1, 1)

		# Update weights and bias
		self.weights += self.eta * error * information_vector
		self.bias += self.eta * error

		# Print diagnostics
		print "Predicted reward: %.2f" % fx
		print "Error: %.2f" % error
		self.print_weights()

	def print_weights(self):
		weight_labels = ['age', 'OSX', 'Windows', 'Linux', 'mobile', 'Google', 'Bing', 'NA ref', 'EN', 'NL', 'GE', 'NA lang', 'price', 'productid', 'green', 'blue', 'red', 'black', 'white', 'skyscraper', 'square', 'banner', '5', '15', '35', 'price_sq']

		for i, x in enumerate(weight_labels):
			print "%s: %.5f" % (x, self.weights[i])

		dic = OrderedDict()

		x = len(weight_labels)
		for i in range(0, len(weight_labels)):
			for j in range(i+1, len(weight_labels)):
				key = weight_labels[i] + "," + weight_labels[j]
				dic[key] = self.weights[x]

				#print "%s, %s: %.5f" % (weight_labels[i], weight_labels[j], self.weights[x])
				x += 1

		foo = OrderedDict(sorted(dic.iteritems(), key=lambda x: x[1]))

		for x in foo:
			if x == "price":
				print x, foo[x]

		print "Bias: %.5f" % self.bias

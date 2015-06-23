from constants import *

import random
import time
import numpy as np
from scipy.optimize import minimize


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


class LinearModel(Model):

	def __init__(self, num_context_variables = 12, num_action_variables = 13, eta = 0.0001):
		num_interactions = (num_context_variables + num_action_variables) * (num_context_variables + num_action_variables - 1) / 2
		self.weights = np.zeros((num_context_variables + num_action_variables + num_interactions))

		# Initialize previous actions array to have warm start when maximizing
		# In order: [price, productid, color, adtype, header]
		# where color is green, adtype is skyscraper and header is 15
		self.prev_actions = np.array([5.00, 18, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0])

		self.bias = 0

		self.num_context_variables = num_context_variables
		self.num_action_variables = num_action_variables

		self.eta = eta
		self.i = 0
		self.random = RandomModel()

	def _one_hot(self, context_key, context_value):
		if context_key == 'Agent':
			return [int(context_value == 'OSX'), int(context_value == 'Windows'), int(context_value == 'Linux'), int(context_value == 'mobile')]
		if context_key == 'Referer':
			return [int(context_value == 'Google'), int(context_value == 'Bing'), int(context_value == 'NA')]
		if context_key == 'Language':
			return [int(context_value == 'EN'), int(context_value == 'NL'), int(context_value == 'GE'), int(context_value == 'NA')]
		if context_key == 'Color':
			return [int(context_value == 'green'), int(context_value == 'blue'), int(context_value == 'red'), int(context_value == 'black'), int(context_value == 'white')]
		if context_key == 'AdType':
			return [int(context_value == 'skyscraper'), int(context_value == 'square'), int(context_value == 'banner')]
		if context_key == 'Header':
			return [int(context_value == 5), int(context_value == 15), int(context_value == 35)]

	def _one_hot_reverse(self, action_key, action_values):
		m = np.argmax(action_values)

		if action_key == 'Header':
			return HEADER_TYPES[m]
		if action_key == 'AdType':
			return AD_TYPES[m]
		if action_key == 'Color':
			return COLOR_TYPES[m]

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
		context_vector = []

		# Append numerical values
		context_vector.append(context['Age'])

		# One-hot encoding
		context_vector += self._one_hot('Agent', context['Agent'])
		context_vector += self._one_hot('Referer', context['Referer'])
		context_vector += self._one_hot('Language', context['Language'])

		context_vector = np.array(context_vector)

		# Create information vector by concatenating the context with the actions
		information_vector = np.concatenate((context_vector, actions))

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
		
		if self.i < 100:
			print "EXPLORATION PHASE %i" % self.i
			return self.random.propose(context)

		print "EXPLOITATION PHASE %i" % self.i

		bounds = [(PRICE_MIN, PRICE_MAX), (PRODUCT_MIN, PRODUCT_MAX), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1)]
		# Use previous action weights as initialization to have a warm start
		result = minimize(self._linear_model, self.prev_actions, args = (context['context']), method = 'L-BFGS-B', bounds = bounds, options = {'maxiter': 1000})

		action = result['x']
		self.prev_actions = action

		return self._one_hot_reverse('Header', action[10:13]), self._one_hot_reverse('AdType', action[7:10]), self._one_hot_reverse('Color', action[2:7]), np.clip(int(np.round(action[1])), PRODUCT_MIN, PRODUCT_MAX), np.clip(action[0], PRICE_MIN, PRICE_MAX)

	def observe(self, context, action, reward):
		# Print to screen in super method
		super(LinearModel, self).observe(context, action, reward)

		action_vector = []

		action_vector.append(action[4]) # price
		action_vector.append(action[3]) # productid

		action_vector += self._one_hot('Color', action[2])
		action_vector += self._one_hot('AdType', action[1])
		action_vector += self._one_hot('Header', action[0])

		# Predicted reward
		fx, information_vector = self._linear_function(action_vector, context['context'])

		# SSE grad
		error = (reward - fx)

		# Ridge
		#error -= np.sum(self.weights) * np.sign(error)

		# Set numerical/ordinal variables to 1 to prevent them from updating faster than dummy variables
		information_vector = np.clip(information_vector, 0, 1)

		# Update weights and bias
		self.weights += self.eta * error * information_vector
		self.bias += self.eta * error

		# Print diagnostics
		print "Predicted reward: %.2f" % fx
		print "Error: %.2f" % error
		self.print_weights()

	def print_weights(self):
		weight_labels = ['age', 'OSX', 'Windows', 'Linux', 'mobile', 'Google', 'Bing', 'NA ref', 'EN', 'NL', 'GE', 'NA lang', 'price', 'productid', 'green', 'blue', 'red', 'black', 'white', 'skyscraper', 'square', 'banner', '5', '15', '35']

		for i, x in enumerate(weight_labels):
			print "%s: %.5f" % (x, self.weights[i])


		x = 25
		for i in range(0, len(weight_labels)):
			for j in range(i+1, len(weight_labels)):
				print "%s, %s: %.5f" % (weight_labels[i], weight_labels[j], self.weights[x])
				x += 1

		print "Bias: %.5f" % self.bias
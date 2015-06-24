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

	def observe(self, context, action, reward):
		pass


class LinearModel(Model):

	def __init__(self, num_context_variables = 12, num_action_variables = 14, eta = 0.00001):
		self.weights = np.random.rand(num_context_variables + num_action_variables)
		#self.weights = np.zeros(num_context_variables + num_action_variables)

		# Initialize previous actions array to have warm start when maximizing
		# In order: [price, productid, color, adtype, header]
		# where color is green, adtype is skyscraper and header is 15
		self.prev_actions = np.array([5.00, 18, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0])

		self.bias = np.random.rand(1)

		self.num_context_variables = num_context_variables
		self.num_action_variables = num_action_variables

		self.eta = eta

		self.bounds = [(AGE_MIN, AGE_MAX), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (PRICE_MIN, PRICE_MAX), (PRODUCT_MIN, PRODUCT_MAX), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (PRICE_MIN**2, PRICE_MAX**2)]

	def _one_hot(self, context_key, context_value):
		if context_key == 'Agent':
			return [int(context_value == 'OSX'), int(context_value == 'Windows'), int(context_value == 'Linux'), int(context_value == 'Mobile')]
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
		information_vector = np.concatenate((information_vector, [actions[0]**2]))

		# Take inner product of weights and information_vector
		y = np.inner(self.weights, information_vector)

		return y, information_vector

	def _linear_model(self, actions, context):
		y, _ = self._linear_function(actions, context)

		# Return negative since we want to maximize instead of minimize
		return -y

	# Override
	def propose(self, context):
		bounds = self.bounds[self.num_context_variables:-1]
		# Use previous action weights as initialization to have a warm start
		result = minimize(self._linear_model, self.prev_actions, args = (context['context']), method = 'L-BFGS-B', bounds = bounds)

		action = result['x']
		self.prev_actions = action

		return self._one_hot_reverse('Header', action[10:13]), self._one_hot_reverse('AdType', action[7:10]), self._one_hot_reverse('Color', action[2:7]), np.clip(int(np.round(action[1])), PRODUCT_MIN, PRODUCT_MAX), np.clip(action[0], PRICE_MIN, PRICE_MAX)

	def observe(self, context, action, reward):
		# Print to screen in super method
		#super(LinearModel, self).observe(context, action, reward)

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

		#information_vector = np.array([v / float(x[1]) for v, x in zip(information_vector, self.bounds)])
		information_vector[information_vector > 0] = 1

		# Ridge
		#error += np.sum(self.weights**2)

		# Update weights
		self.weights += self.eta * error * information_vector
		#print reward, fx
		#print error, self.weights

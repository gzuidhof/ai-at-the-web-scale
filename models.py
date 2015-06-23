from constants import *

import random
import time
import numpy as np


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
	# Override
	def propose(self, context):

		### minimize

		return header, adtype, color, product_id, price

	# Override
	def observe(self, context, action, reward):
		pass
		### update model
	
import numpy as np
import sklearn.linear_model
import models
import matplotlib.pyplot as plt


if __name__ == "__main__":
	X = np.load("vectors.npy")
	y = np.load("rewards.npy")

	lin = sklearn.linear_model.Ridge()
	lin.fit(X, y)
	print lin.score(X, y)

	la = models.LinearModel()
	la.weights = lin.coef_

	la.print_weights()

	np.save("weights.npy", lin.coef_)
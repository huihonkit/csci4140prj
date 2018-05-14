import numpy as np
from sklearn.linear_model import LogisticRegression
from random import randint
import random
from sklearn.externals import joblib

#clf3 = joblib.load('save/clf.pkl')

#generate train data
X = []
#Y = []
for i in range(100):
	est = randint(0, 25)
	credit  = randint(0, 100)
	X.append([est, credit, 1])
	#Y.append(1)

for i in range(100):
	est = randint(-25, 0)
	credit = randint(0, 100)
	X.append([est, credit, 1])
	#Y.append(1)

for i in range(100):
	est = randint(-25, 0)
	credit = randint(-10, 0)
	X.append([est, credit,randint(0, 1)])
	#Y.append(randint(0, 1))

for i in range(100):
	est = randint(-100, -50)
	credit = randint(100, 150)
	X.append([est, credit, 1])
	#Y.append(1)

for i in range(100):
	est = randint(-100, -50)
	credit = randint(-100,-1)
	X.append([est, credit, 0])
	#Y.append(0)

model = LogisticRegression()
random.shuffle(X)
X = np.array(X)
Y = X[:,2:]
X = X[:,0:2]

X_train = X[:200]
Y_train = Y[:200]

model.fit(X_train, Y_train)

X_test = X[-100:]
Y_test = Y[-100:]
print(model.score(X_test, Y_test))
joblib.dump(model, 'save/model.pkl')



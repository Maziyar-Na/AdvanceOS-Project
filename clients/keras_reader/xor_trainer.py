from keras.models import Sequential
from keras.layers.core import Activation, Dense
from keras.optimizers import SGD

X = np.zeros((4, 2), dtype='uint8')
y = np.zeros(4, dtype='uint8')

X[0] = [0, 0]
y[0] = 0
X[1] = [0, 1]
y[1] = 1
X[2] = [1, 0]
y[2] = 1
X[3] = [1, 1]
y[3] = 0

model = Sequential()
model.add(Dense(2, input_dim=2))
model.add(Activation('sigmoid'))
model.add(Dense(1))
model.add(Activation('sigmoid'))
sgd = SGD(lr=0.01)
model.compile(loss='binary_crossentropy', optimizer=sgd)
model.fit(X, y, nb_epoch=100000, batch_size=1)
print(model.predict_proba(X))

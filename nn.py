"""
The design of this comes from here:
http://outlace.com/Reinforcement-Learning-Part-3/
"""

from keras.models import Sequential, Model
from keras.layers.core import Dense, Activation, Dropout, Reshape
from keras.layers import Dense, Input
from keras.optimizers import RMSprop, sgd
from keras.layers.recurrent import LSTM
from keras.callbacks import Callback


class LossHistory(Callback):
    def on_train_begin(self, logs={}):
        self.losses = []

    def on_batch_end(self, batch, logs={}):
        self.losses.append(logs.get('loss'))


def neural_net(num_sensors, params, load = ''):
    a = Input(shape=(2,))
    b = Dense(128, activation='relu')(a)
    c = Dense(64, activation='relu')(b)
    d = Dense(5, activation='linear')(c)

    model = Model(inputs = a, outputs = d)
    model.summary()
    model.compile(loss='mse', optimizer = 'sgd')

    if load:
        model.load_weights(load)
    return model


def neural_net1(num_sensors, params, load=''):
    model = Sequential()

    # First layer.
    model.add(Dense(
        params[0], init='lecun_uniform', input_shape=(num_sensors,)
    ))
    model.add(Activation('relu'))
    # model.add(Dropout(0.2))

    # Second layer.
    model.add(Dense(params[1], init='lecun_uniform', name = '1'))
    model.add(Activation('relu', name = '3'))
    # model.add(Dropout(0.2))
    # Third layer.
    model.add(Dense(params[2], init='lecun_uniform', name = '2'))
    model.add(Activation('relu', name = '4'))
    # model.add(Dropout(0.2))

    # Output layer.
    model.add(Dense(5, init='lecun_uniform', name = '5'))
    model.add(Reshape((5,)))
    # model.add(Activation('linear', name = '6'))
    model.summary()
    rms = RMSprop()
    model.compile(loss='mse', optimizer=rms)

    if load:
        model.load_weights(load)

    return model

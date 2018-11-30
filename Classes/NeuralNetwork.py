# import modules
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

import numpy as np
import tensorflow as tf
from tensorflow.python.keras import models, layers, initializers, regularizers, optimizers, backend

# constants
BATCH_SIZE = 128
EPOCHS = 10
CHANNEL_AXIS = -1
CONV_FILTER_SIZE = 64
RES_FILTER_SIZE = 64
# FILTER_SIZE = 8
NUM_POSSIBLE_MOVES = 52
KERNEL_INITIALIZER = initializers.RandomUniform()
KERNEL_REGULIZER = regularizers.l2()

class NeuralNetwork:
    def __init__(self):
        self.load_checkpoint()    # loads saved model if there is any.

    '''
    ### MAIN FUNCTIONS ###
    '''
    def build_network(self):
        print("Building Model")
        _input = layers.Input(shape=(17, 17))

        def common_layer(_input):
            return layers.Activation("relu")(layers.BatchNormalization(axis=CHANNEL_AXIS)(_input))

        def conv_block(_input, filters=64, kernel=(4, 4), strides=2, padding='same'):
            return common_layer(layers.Conv2D(filters=filters, kernel_size=kernel,
                                             strides=strides, padding=padding,
                                             kernel_initializer=KERNEL_INITIALIZER,
                                             kernel_regularizer=KERNEL_REGULIZER)(_input))

        def residual_block(_input):
            shortcut = _input
            conv1 = conv_block(_input, filters=RES_FILTER_SIZE, kernel=(4,4), strides=1)
            conv2 = conv_block(conv1, filters=RES_FILTER_SIZE, kernel=(4,4), strides=1)
            out = layers.add([shortcut, conv2])
            return out

        def policy_head(_input):
            conv1 = conv_block(_input, filters=2, kernel=(1, 1), strides=1)
            out = layers.Dense(units=NUM_POSSIBLE_MOVES, activation='softmax')(conv1)
            return out

        def value_head(_input):
            conv1 = conv_block(_input, filters=1, kernel=1, strides=1)
            flat = tf.layers.flatten(conv1)
            dense1 = layers.Dense(units=256, activation='relu')(flat)
            print("dense1: {}".format(dense1.shape))
            out = layers.Dense(units=1, activation='sigmoid')(dense1)
            print("out: {}".format(out.shape))
            return out

        # main blocks
        reshape = layers.Reshape((17, 17, 1))(_input)
        conv1 = conv_block(reshape, filters=CONV_FILTER_SIZE)
        res1 = residual_block(conv1)
        res2 = residual_block(res1)
        res3 = residual_block(res2)
        res4 = residual_block(res3)
        res5 = residual_block(res4)
        res6 = residual_block(res5)
        res7 = residual_block(res6)
        res8 = residual_block(res7)
        res9 = residual_block(res8)
        # p = policy_head(res5)
        v = value_head(res9)

        # default parameters for optimizer: lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False
        model = tf.keras.Model(inputs=[_input], outputs=v)
        return model.compile(loss='mean_squared_error', optimizer=optimizers.Adam())


    def train_network(self, _input, z):
        # return model.fit(x = states, y = [pi, z], batch_size = BATCH_SIZE, epochs = EPOCHS)
        self.model.fit(x=_input, y=z, batch_size=BATCH_SIZE, epochs=EPOCHS)
        self.save_checkpoint()
        print("Training finished for {}".format(EPOCHS))


    def predict_values(self, player, opponent, center):
        _input = self.state2input(player, opponent, center)
        _input = np.expand_dims(_input, axis=0)
        return self.model.predict([_input])

    def predict_input_values(self, _input):
        return self.model.predict([_input])

    '''
    ### UTILITY FUNCTIONS ###
    '''
    def state2input(self, player, opponent, center):
        # score ( 2 x 17 )
        _score = np.zeros((2, 17))
        for card in player.cards:
            if card.suit == 0:
                _score[0][card.value - 1] += 1
            elif card.value == 1:
                _score[0][card.suit + 13 - 1] += 1
            elif card.suit == 3 and card.value == 10:
                _score[0][16] += 1
        for card in opponent.cards:
            if card.suit == 0:
                _score[1][card.value - 1] += 1
            elif card.value == 1:
                _score[1][card.suit + 13 - 1] += 1
            elif card.suit == 3 and card.value == 10:
                _score[1][16] += 1
        # score = np.expand_dims(score, axis=2)

        # hand ( 2 x 17 )
        _hand = np.zeros((2, 17))
        for card in player.hand:
            if card.suit == 0:
                _hand[0][card.value - 1] += 1
            elif card.value == 1:
                _hand[0][card.suit + 13 - 1] += 1
            elif card.suit == 3 and card.value == 10:
                _hand[0][16] += 1
            else:
                _hand[1][card.value-2] += 1   # last 5 will be padded with zeros
        # hand = np.expand_dims(hand, axis=2)

        # center ( 13 x 17 )
        _center = np.zeros((13, 17))
        for index, pile in enumerate(center.piles):
            for card in pile.cards:
                if card.suit == 0:
                    _center[12-index][card.value - 1] += 0.5
                elif card.value == 1:
                    _center[12-index][card.suit + 13 - 1] += 0.5
                elif card.suit == 3 and card.value == 10:
                    _center[12-index][16] += 0.5
            _center[12-index][pile.value] += 1

        _input = np.append(_center, _hand, axis=0)
        _input = np.append(_input, _score, axis=0)
        # centerVector = centerVector[~np.all(centerVector == 0, axis=1)]
        # _center = np.expand_dims(_center, axis=2)

        return _input

    def show_model_summary(self):
        if self.model is None:
            return
        self.model.summary()

    def save_checkpoint(self, folder='checkpoint', filename='nn_model.h5'):
        filepath = os.path.join(folder, filename)
        if not os.path.exists(folder):
            print("Checkpoint Directory does not exist! Making directory {}".format(folder))
            os.mkdir(folder)
        else:
            print("Checkpoint Directory exists! ")
        models.save_model(self.model, filepath)

    def load_checkpoint(self, folder='checkpoint', filename='nn_model.h5'):
        filepath = os.path.join(folder, filename)
        if not os.path.exists(filepath):
            print("No model in path {}".format(filepath))
            self.model = self.build_network()
        else:
            self.model = models.load_model(filepath)

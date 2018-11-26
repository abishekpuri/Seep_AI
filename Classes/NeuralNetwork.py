# import modules
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import models, layers, initializers, regularizers, optimizers, backend

# constants
BATCH_SIZE = 128
EPOCHS = 10
CHANNEL_AXIS = -1
CONV_FILTER_SIZE = 32
RES_FILTER_SIZE = 32
FILTER_SIZE = 8
NUM_POSSIBLE_MOVES = 52
KERNEL_INITIALIZER = initializers.RandomUniform()
KERNEL_REGULIZER = regularizers.l2()

class NeuralNetwork:
    def __init__(self):
        self.model = None
        self.loadCheckpoint()    # loads saved model every time

    '''
    ### MAIN FUNCTIONS ###
    '''
    def buildNetwork(self):
        # Convolutional layer for 3 inputs (score, hand, center)
        scoreInput = layers.Input(shape=(2, 17))
        handInput = layers.Input(shape=(29, ))
        centerInput = layers.Input(shape=(6, 17))

        def commonLayer(_input):
            return layers.Activation("relu")(layers.BatchNormalization(axis=CHANNEL_AXIS)(_input))

        def convBlock1D(_input, filters=16, kernel=4, strides=2, padding='same'):
            return commonLayer(layers.Conv1D(filters=filters, kernel_size=kernel,
                                             strides=strides, padding=padding,
                                             kernel_initializer=KERNEL_INITIALIZER,
                                             kernel_regularizer=KERNEL_REGULIZER)(_input))

        def convBlock2D(_input, filters=16, kernel=(2, 4), strides=2, padding='same'):
            return commonLayer(layers.Conv2D(filters=filters, kernel_size=kernel,
                                             strides=strides, padding=padding,
                                             kernel_initializer=KERNEL_INITIALIZER,
                                             kernel_regularizer=KERNEL_REGULIZER)(_input))

        def scoreConvLayer(score):
            reshaped = layers.Reshape((2, 17, 1))(score)
            convBlock1 = convBlock2D(reshaped)
            convBlock2 = convBlock2D(convBlock1)
            convBlock3 = convBlock2D(convBlock2)
            convBlock4 = convBlock2D(convBlock3)
            print("Structure of score conv layer")
            print("convBlock1: {}".format(convBlock1.shape))
            print("convBlock2: {}".format(convBlock2.shape))
            print("convBlock3: {}".format(convBlock3.shape))
            print("convBlock4: {}".format(convBlock4.shape))
            return tf.layers.flatten(convBlock4)

        def handConvLayer(hand):
            print("Structure of hand conv layer")
            reshaped = layers.Reshape((29, 1))(hand)
            convBlock1 = convBlock1D(reshaped)
            convBlock2 = convBlock1D(convBlock1)
            convBlock3 = convBlock1D(convBlock2)
            convBlock4 = convBlock1D(convBlock3)
            print("convBlock1: {}".format(convBlock1.shape))
            print("convBlock2: {}".format(convBlock2.shape))
            print("convBlock3: {}".format(convBlock3.shape))
            print("convBlock4: {}".format(convBlock4.shape))
            return tf.layers.flatten(convBlock4)

        # TODO: how to reduce redundacy for piles > 5
        def centerConvLayer(center):
            print("Structure of center conv layer")
            reshaped = layers.Reshape((6, 17, 1))(center)
            convBlock1 = convBlock2D(reshaped)
            convBlock2 = convBlock2D(convBlock1)
            convBlock3 = convBlock2D(convBlock2)
            convBlock4 = convBlock2D(convBlock3)
            print("convBlock1: {}".format(convBlock1.shape))
            print("convBlock2: {}".format(convBlock2.shape))
            print("convBlock3: {}".format(convBlock3.shape))
            print("convBlock4: {}".format(convBlock4.shape))
            return tf.layers.flatten(convBlock4)

        def shConvLayer(sh):
            print("Structure of sh conv layer")
            reshaped = layers.Reshape((2, 32, 1))(sh)
            convBlock1 = convBlock2D(reshaped)
            convBlock2 = convBlock2D(convBlock1)
            convBlock3 = convBlock2D(convBlock2)
            convBlock4 = convBlock2D(convBlock3)
            print("convBlock1: {}".format(convBlock1.shape))
            print("convBlock2: {}".format(convBlock2.shape))
            print("convBlock3: {}".format(convBlock3.shape))
            print("convBlock4: {}".format(convBlock4.shape))
            return tf.layers.flatten(convBlock4)

        def hcConvLayer(hc):
            print("Structure of hc conv layer")
            reshaped = layers.Reshape((2, 32, 1))(hc)
            convBlock1 = convBlock2D(reshaped)
            convBlock2 = convBlock2D(convBlock1)
            convBlock3 = convBlock2D(convBlock2)
            convBlock4 = convBlock2D(convBlock3)
            print("convBlock1: {}".format(convBlock1.shape))
            print("convBlock2: {}".format(convBlock2.shape))
            print("convBlock3: {}".format(convBlock3.shape))
            print("convBlock4: {}".format(convBlock4.shape))
            return tf.layers.flatten(convBlock4)

        def shcConvLayer(shc):
            print("Structure of shc conv layer")
            reshaped = layers.Reshape((2, 32, 1))(shc)
            convBlock1 = convBlock2D(reshaped)
            convBlock2 = convBlock2D(convBlock1)
            convBlock3 = convBlock2D(convBlock2)
            convBlock4 = convBlock2D(convBlock3)
            print("convBlock1: {}".format(convBlock1.shape))
            print("convBlock2: {}".format(convBlock2.shape))
            print("convBlock3: {}".format(convBlock3.shape))
            print("convBlock4: {}".format(convBlock4.shape))
            return tf.layers.flatten(convBlock4)

        def resBlock1D(_input):
            shortcut = _input
            convBlock1 = convBlock1D(_input, filters=RES_FILTER_SIZE, kernel=3, strides=1)
            convBlock2 = convBlock1D(convBlock1, filters=RES_FILTER_SIZE, kernel=3, strides=1)
            out = layers.add([shortcut, convBlock2])
            return out

        def policyHead(_input):
            convBlock1 = convBlock1D(_input, filters=2, kernel=1, strides=1)
            out = layers.Dense(units=NUM_POSSIBLE_MOVES, activation='softmax')(convBlock1)
            return out

        def valueHead(_input):
            reshaped = layers.Reshape((16, 32, 1))(_input)
            convBlock1 = convBlock2D(reshaped, filters=1, kernel=1, strides=1)
            flat = tf.layers.flatten(convBlock1)
            print("convBlock1: {}".format(flat.shape))
            dense1 = layers.Dense(units=512, input_shape=(512,), activation='relu')(flat)
            print("dense1: {}".format(dense1.shape))
            out = layers.Dense(units=1, activation='sigmoid')(dense1)
            print("out: {}".format(out.shape))
            return out

        # combine outputs of 3 different conv layers
        '''
        scoreFeature: (?, 32)
        handFeature: (?, 32)
        centerFeature: (?, 32)
        '''
        # Block 1
        scoreFeature = scoreConvLayer(scoreInput)
        handFeature = handConvLayer(handInput)
        centerFeature = centerConvLayer(centerInput)
        print("Shape of scoreFeature: {}".format(scoreFeature.shape))
        shInput = layers.concatenate([scoreFeature, handFeature], axis=1)
        print("Shape of shInput: {}".format(shInput.shape))
        hcInput = layers.concatenate([handFeature, centerFeature], axis=1)
        print("Shape of hcInput: {}".format(hcInput.shape))

        # Block 2
        shFeature = shConvLayer(shInput)
        hcFeature = hcConvLayer(hcInput)
        shcInput = layers.concatenate([shFeature, hcFeature], axis=1)

        # Block 3
        shcFeature = shcConvLayer(shcInput)
        mainInput = layers.Reshape((shcFeature.shape[1], 1))(shcFeature)
        print("Shape of mainInput: {}".format(mainInput.shape))

        # main blocks
        conv = convBlock1D(mainInput, filters=CONV_FILTER_SIZE)
        res1 = resBlock1D(conv)
        res2 = resBlock1D(res1)
        res3 = resBlock1D(res2)
        res4 = resBlock1D(res3)
        res5 = resBlock1D(res4)
        # p = policy_head(res5)
        v = valueHead(res5)

        # default parameters for optimizer: lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False
        self.model = tf.keras.Model(inputs=[scoreInput, handInput, centerInput], outputs=v)
        self.model.compile(loss='mean_squared_error', optimizer=optimizers.Adam())


    def trainNetwork(self, _score, _hand, _center, z):
        # return model.fit(x = states, y = [pi, z], batch_size = BATCH_SIZE, epochs = EPOCHS)
        for i in range(10):
            self.model.fit(x=[_score, _hand, _center], y=z, batch_size=BATCH_SIZE, epochs=EPOCHS)
            self.saveCheckpoint()
            print("Training finished for {}".format(EPOCHS * i))
        print("Training finished for {}".format(EPOCHS*10))


    def predict(self, player, opponent, center):
        _score, _hand, _center = self.stateToInput(player, opponent, center)
        _score = np.expand_dims(_score, axis=0)
        _hand = np.expand_dims(_hand, axis=0)
        _center = np.expand_dims(_center, axis=0)
        predictWin = self.model.predict([_score, _hand, _center])
        print(predictWin)

    '''
    ### UTILITY FUNCTIONS ###
    '''
    def stateToInput(self, player, opponent, center):
        # score ( 2 x 17 )
        score = np.zeros((2, 17))
        for card in player.cards:
            if card.suit == 0:
                score[0][card.value - 1] += 1
            elif card.value == 1:
                score[0][card.suit + 13 - 1] += 1
            elif card.suit == 3 and card.value == 10:
                score[0][16] += 1
        for card in opponent.cards:
            if card.suit == 0:
                score[1][card.value - 1] += 1
            elif card.value == 1:
                score[1][card.suit + 13 - 1] += 1
            elif card.suit == 3 and card.value == 10:
                score[1][16] += 1
        # score = np.expand_dims(score, axis=2)

        # hand ( 1 x 29 )
        hand = np.zeros(29)
        for card in player.hand:
            if card.suit == 0:
                hand[card.value - 1] += 1
                print("Spade {}".format(card.value))
            elif card.value == 1:
                hand[card.suit + 13 - 1] += 1
            elif card.suit == 3 and card.value == 10:
                hand[16] += 1
            else:
                hand[card.value + 17 - 1] += 1
        # hand = np.expand_dims(hand, axis=2)

        # center ( 6 x 17 )
        _center = np.zeros((6, 17))
        for index, pile in enumerate(center.piles):
            if index > 5:
                print("There are more than 6 piles !!!")
                break
            for card in pile.cards:
                if card.suit == 0:
                    _center[index][card.value - 1] += 0.5
                elif card.value == 1:
                    _center[index][card.suit + 13 - 1] += 0.5
                elif card.suit == 3 and card.value == 10:
                    _center[index][16] += 0.5
            _center[index][pile.value] += 1

        # centerVector = centerVector[~np.all(centerVector == 0, axis=1)]
        # _center = np.expand_dims(_center, axis=2)

        return score, hand, _center

    def showModelSummary(self):
        if self.model is None:
            return
        self.model.summary()

    def saveCheckpoint(self, folder='checkpoint', filename='nn_model.h5'):
        filepath = os.path.join(folder, filename)
        if not os.path.exists(folder):
            print("Checkpoint Directory does not exist! Making directory {}".format(folder))
            os.mkdir(folder)
        else:
            print("Checkpoint Directory exists! ")
        models.save_model(self.model, filepath)

    def loadCheckpoint(self, folder='checkpoint', filename='nn_model.h5'):
        filepath = os.path.join(folder, filename)
        if not os.path.exists(filepath):
            raise ("No model in path {}".format(filepath))
        self.model = models.load_model(filepath)
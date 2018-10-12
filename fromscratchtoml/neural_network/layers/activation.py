#!/usr/bin/env python
# -*- coding: utf-8 -*-
#



from functools import partial

from .. import Activations
from . import Layer

import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Activation(Layer):
    """
    This is where the activation is applied at the raw output of the perceptrons.

    Examples
    --------
    >>> from fromscratchtoml.neural_network.models import Sequential
    >>> from fromscratchtoml.neural_network.optimizers import StochasticGradientDescent
    >>> from fromscratchtoml.neural_network.layers import Dense, Activation
    >>> X1 = np.array([[0, 0],[0, 1],[1, 0], [1, 1]])
    >>> y1 = np.array([[1,0], [0,1], [0,1], [1,0]])
    >>> model = Sequential()
    >>> model.add(Dense(5, input_dim=2, seed=1))
    >>> model.add(Activation('sigmoid'))
    >>> model.add(Dense(5, seed=2))
    >>> model.add(Activation('sigmoid'))
    >>> model.add(Dense(2, seed=3))
    >>> sgd = StochasticGradientDescent(learning_rate=0.1)
    >>> model.compile(optimizer=sgd, loss="mean_squared_error")
    >>> model.fit(X1, y1, batch_size=4, epochs=100)
    >>> model.predict(X1, one_hot=True)
    """
    def __init__(self, activation, trainable=False):
        """
        Initialising the layer parameters.

        Parameters
        ----------
        activation : string
            The activation function to be used.
        trainable : bool, optional
            This is only present to mantain consistency amongst the layer structure, this parameter has no effect since
            there are no weights to be updated or trained.

        """
        self.activation = partial(getattr(Activations, activation))

    def forward(self, X, train=False):
        """
        Forward pass the output of the previous layer by applying activation function to it.

        Parameters
        ----------
        X : numpy.ndarray
            The ouput of the previous layer.
        return_deriv : bool, optional
            If set to true, the function returns derivative of the output along with the output.

        Returns
        -------
        numpy.array : The activated ouput.
        """
        self.input = X
        self.output, self.output_deriv = self.activation(X, return_deriv=True)

        return self.output

    def back_propogate(self, dEdO):
        """
        Backpropogate the error, this function adds the share of activation layer to the accumulated delta.

        Parameters
        ----------
        dEdO : numpy.ndarray
            The accumulated delta used for calculating error gradient with respect to parameters.

        Returns
        -------
        numpy.array : The accumulated delta.
        """

        dEdO = dEdO * self.output_deriv

        return dEdO

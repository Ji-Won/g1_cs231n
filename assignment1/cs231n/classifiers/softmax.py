import numpy as np
from random import shuffle
from past.builtins import xrange

def softmax_loss_naive(W, X, y, reg):
  """
  Softmax loss function, naive implementation (with loops)

  Inputs have dimension D, there are C classes, and we operate on minibatches
  of N examples.

  Inputs:
  - W: A numpy array of shape (D, C) containing weights.
  - X: A numpy array of shape (N, D) containing a minibatch of data.
  - y: A numpy array of shape (N,) containing training labels; y[i] = c means
    that X[i] has label c, where 0 <= c < C.
  - reg: (float) regularization strength

  Returns a tuple of:
  - loss as single float
  - gradient with respect to weights W; an array of same shape as W
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using explicit loops.     #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  num_classes = W.shape[1]
  num_train = X.shape[0]
  loss = 0.0
  for i in xrange(num_train):
    scores = X[i].dot(W)
    scores -= np.max(scores)
    scores = np.exp(scores)
    p = scores[y[i]]/np.sum(scores)
    loss += -np.log(p)
    for j in xrange(num_classes):
        dW[:,j] += (scores[j]/np.sum(scores))*X[i] #gradient update for incorrect rows
        
        if j == y[i]:
            dW[:,j] -= X[i]
    
  # Right now the loss is a sum over all training examples, but we want it
  # to be an average instead so we divide by num_train.
  loss /= num_train
  dW /= num_train
  dW += 2*reg*W # regularize the weights

  # Add regularization to the loss.
  loss += 0.5*reg * np.sum(W * W)
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
  """
  Softmax loss function, vectorized version.

  Inputs and outputs are the same as softmax_loss_naive.
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  num_train = X.shape[0]
  scores = X.dot(W)
  scores -= np.amax(scores, axis =1, keepdims = True)
  scores = np.exp(scores)
  sum_scores = np.sum(scores, axis=1, keepdims=True)
  probs = scores[np.arange(num_train), y]/np.ndarray.flatten(sum_scores)
  loss = np.sum(-np.log(probs))

  p = scores / sum_scores
  ind = np.zeros_like(p)
  ind[np.arange(num_train), y] = 1
  Q = p - ind
  dW = X.T.dot(Q)

  loss /= num_train
  dW /= num_train
  dW += 2*reg*W # regularize the weights
  # Add regularization to the loss.
  loss += 0.5*reg * np.sum(W * W)
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW


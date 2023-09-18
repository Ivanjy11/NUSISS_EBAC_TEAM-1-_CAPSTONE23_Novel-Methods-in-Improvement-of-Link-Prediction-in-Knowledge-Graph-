import tensorflow as tf
import numpy as np

class Baseline(object):
    def get_baseline_value(self):
        pass

    def update(self, target):
        pass

class ReactiveBaseline(Baseline):
    def __init__(self, l):
        self.l = l
        self.b = tf.Variable(0.0, trainable=False)

    def get_baseline_value(self):
        return self.b

    def update(self, target):
        self.b.assign((1 - self.l) * self.b + self.l * target)

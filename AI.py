import math

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense


class AI:

    def randomize_network(self):
        self.model = Sequential([
            Dense(128, activation='relu', input_shape=(211,)),
            Dense(64, activation='sigmoid'),
            Dense(1, activation='sigmoid')
        ])

    def __init__(self):
        self.model = None

    #   0-> do nothing; 1-> move right; 2-> move left; 3-> rotate right; 4-> rotate left
    def get_move(self, board, next_piece, piece):
        flatten_1 = np.array(board).reshape(-1)
        flatten_2 = np.array(piece[1]).reshape(-1)
        flatten_3 = np.array([next_piece, piece[0], piece[2]])
        combine = np.concatenate((flatten_1, flatten_2, flatten_3))
        combine = combine.reshape(1, -1)
        prediction = self.model.predict(combine)
        move = math.floor(prediction[0][0] * 5)
        print(prediction, move)
        return move


def main():
    ai = AI()
    ai.randomize_network()


if __name__ == "__main__":
    main()

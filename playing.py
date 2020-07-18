"""
Once a model is learned, use this to play it.
"""
import random
import carmunk
import numpy as np
from nn import neural_net

NUM_SENSORS = 18


def play(model):

    car_distance = 0
    game_state = carmunk.GameState()

    # Do nothing to get initial.
    _, state = game_state.frame_step((2))

    # Move.
    while True:
        car_distance += 1

        # Choose action.
        #action = (np.argmax(model.predict(state, batch_size=1)))

        # Take action.
        
        if random.random() < 0.4:
            action = np.random.randint(0, 3)  # random
        else:
            # Get Q values for each action.
            qval = model.predict(state, batch_size=1)
            action = (np.argmax(qval))  # best
        
        _, state = game_state.frame_step(action)
        
        # Tell us something.
        if car_distance % 1000 == 0:
            print("Current distance: %d frames." % car_distance)


if __name__ == "__main__":
    saved_model = 'saved-models/128-128-64-50000-100000.h5'
    model = neural_net(NUM_SENSORS, [128, 128,128], saved_model)
    play(model)

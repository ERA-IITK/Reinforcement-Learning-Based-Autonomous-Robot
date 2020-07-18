from flat_game import carmunk
import numpy as np
import random
import csv
from nn import neural_net, LossHistory
import os.path
import timeit
# import keyboard

NUM_INPUT = 2#?
GAMMA = 0.9  # Forgetting.
TUNING = False  # If False, just use arbitrary, pre-selected params.
learning_rate = 0.45

def train_net(model, params):

    filename = params_to_filename(params)
    observe = 128  # Number of frames to observe before training.
    epsilon = 1
    train_frames = 11000000 # Number of frames to play.
    steps = 0
    batchSize = params['batchSize']
    buffer = params['buffer']

    # Just stuff used below.
    max_car_distance = 0
    car_distance = 0
    t = 0
    data_collect = []
    replay = []  # stores tuples of (S, A, R, S'). #to be displayed 

    loss_log = []

    # Create a new game instance.
    game_state = carmunk.GameState()

    # Get initial state by doing nothing and getting the state.
    _, state, _ = game_state.frame_step((2))

    # Let's time it.
    start_time = timeit.default_timer()

    # Run the frames.
    
    while t < train_frames:

        t += 1
        car_distance += 1
        print(t)
        # Choose an action.
        if random.random() < epsilon or t < observe:
            action = np.random.randint(0, 5)  # random
        else:
            # Get Q values for each action.
            qval = model.predict(state, batch_size=1)
            action = (np.argmax(qval))  # best

        # Take action, observe new state and get our treat.
        reward, new_state,term = game_state.frame_step(action)
        # print(t, reward, action)
        # Experience replay storage.
        replay.append((state, action, reward, new_state))
        # print(len(replay))
        # If we're done observing, start training.
        if t > observe:
            #print("start")
            # If we've stored enough in our buffer, pop the oldest.
            if len(replay) > buffer:
                replay.pop(0)

            # Randomly sample our experience replay memory
            minibatch = random.sample(replay, batchSize)

            # Get training values.
            X_train, y_train = process_minibatch2(minibatch, model)
            # Train the model on this batch.
            history = LossHistory()
            model.fit(
                X_train, y_train, batch_size=batchSize,
                nb_epoch=1, verbose=0, callbacks=[history]
            )
            loss_log.append(history.losses)
            steps += 1
            if steps % 1000 == 0:
                print("Step = " + str(steps),"Epsilon = "+str(epsilon))
        # Update the starting state with S'.
        state = new_state

        # Decrement epsilon over time.
        if epsilon > 0.1 and t > observe:
            epsilon -= (1.0/train_frames)

        # We died, so update stuff.
        if term ==1 :
            # print("Crashed.")
            # Log the car's distance at this T.
            data_collect.append([t, car_distance])
            continue
            # Reset.
            car_distance = 0
        # We reached the goal, so update stuff.
        elif term==2:
            print("Reached goal.", car_distance)
            # Log the car's distance at this T.
            data_collect.append([t, car_distance])
            continue
            # Reset.
            car_distance = 0

        # Save the model every 25,000 frames.
        if t % 25000 == 0:
            model.save_weights('saved-models/' + filename + '-' +
                               str(t) + '.h5',
                               overwrite=True)
            print("Saving model %s - %d" % (filename, t))
        # if(keyboard.is_pressed('8')):
        #     print("Reset Goal")
        #     game_state.reset_goal()


    # Log results after we're done all frames.
    #log_results(filename, data_collect, loss_log)


def log_results(filename, data_collect, loss_log):
    # Save the results to a file so we can graph it later.
    with open('results/sonar-frames/learn_data-' + filename + '.csv', 'a+') as data_dump:
        wr = csv.writer(data_dump)
        wr.writerows(data_collect)

    with open('results/sonar-frames/loss_data-' + filename + '.csv', 'a+') as lf:
        wr = csv.writer(lf)
        for loss_item in loss_log:
            wr.writerow(loss_item)

def process_minibatch2(minibatch, model):
    # by Microos, improve this batch processing function 
    #   and gain 50~60x faster speed (tested on GTX 1080)
    #   significantly increase the training FPS
    
    # instead of feeding data to the model one by one, 
    #   feed the whole batch is much more efficient

    mb_len = len(minibatch)

    old_states = np.zeros(shape=(mb_len, NUM_INPUT))
    actions = np.zeros(shape=(mb_len,))
    rewards = np.zeros(shape=(mb_len,))
    new_states = np.zeros(shape=(mb_len, NUM_INPUT))

    for i, m in enumerate(minibatch):
        old_state_m, action_m, reward_m, new_state_m = m
        old_states[i, :] = old_state_m[:]
        actions[i] = action_m
        rewards[i] = reward_m
        new_states[i, :] = new_state_m[:]

    old_qvals = model.predict(old_states, batch_size=mb_len)
    new_qvals = model.predict(new_states, batch_size=mb_len)
    old_qvals_max = []
    new_qvals_max = []
    # print(old_qvals)
    # for list_e in old_qvals:
    #     old_qvals_max.append(max(list_e))
    # for list_e in new_qvals:
    #     new_qvals_max.append(max(list_e)) 
 
    maxQs = np.maximum(new_qvals, old_qvals)
    print(maxQs)
    # y = old_qvals
    # non_term_inds = np.where(rewards != 300)[0]
    # term_inds = np.where(rewards == 300)[0]
    # self.q[state,action]=self.q[state,action] -self.step_size*(rward+self.discount*max(self.q[state_new,:])-self.q[state,action])
    for i in range(mb_len):
        actions[i] = int(actions[i])
        old_qvals[i][actions[i]] = new_qvals[i][actions[i]] + learning_rate * (rewards[i] + (GAMMA * maxQs[i][actions[i]]) - old_qvals[i][actions[i]])
    # y[non_term_inds, actions[non_term_inds].astype(int)] = rewards[non_term_inds] + (GAMMA * maxQs[non_term_inds])
    # y[term_inds, actions[term_inds].astype(int)] = rewards[term_inds]

    X_train = old_states
    y_train = old_qvals

    # y_train=(y_train.reshape(5))
    # print(old_qvals)
    return X_train, y_train

def params_to_filename(params):
    return str(params['nn'][0]) + '-' + str(params['nn'][1]) + '-' + \
            str(params['batchSize']) + '-' + str(params['buffer'])


def launch_learn(params):
    filename = params_to_filename(params)
    print("Trying %s" % filename)
    # Make sure we haven't run this one.
    if not os.path.isfile('results/sonar-frames/loss_data-' + filename + '.csv'):
        # Create file so we don't double test when we run multiple
        # instances of the script at the same time.
        open('results/sonar-frames/loss_data-' + filename + '.csv', 'a').close()
        print("Starting test.")
        # Train.
        model = neural_net(NUM_INPUT, params['nn'])
        train_net(model, params)
    else:
        print("Already tested.")


if __name__ == "__main__":
    if TUNING:
        param_list = []
        nn_params = [[164, 150], [256, 256],
                     [512, 512], [1000, 1000]]
        batchSizes = [40, 100, 400]
        buffers = [10000, 50000]

        for nn_param in nn_params:
            for batchSize in batchSizes:
                for buffer in buffers:
                    params = {
                        "batchSize": batchSize,
                        "buffer": buffer,
                        "nn": nn_param
                    }
                    param_list.append(params)

        for param_set in param_list:
            launch_learn(param_set)

    else:
        nn_param = [128, 128,128]
        params = {
            "batchSize": 128,
            "buffer": 50000,
            "nn": nn_param
        }
        model = neural_net(NUM_INPUT, nn_param)
        train_net(model, params)

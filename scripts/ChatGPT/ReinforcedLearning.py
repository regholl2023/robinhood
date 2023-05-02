#!/usr/bin/python

import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from math import sqrt
import gym
from gym import spaces
from stable_baselines3 import A2C
from stable_baselines3.common.env_checker import check_env

def ReinforcedLearning(i_df):

    # Create a copy of df to prevent overwrite
    data = i_df.copy(deep=True)
    data = data.filter(['Close']).values

    # Preprocess the data
    scaler = MinMaxScaler(feature_range=(0, 1))
    data = scaler.fit_transform(data)

    # Split the data into training and testing sets
    train_size = int(len(data) * 0.8)
    train_data = data[:train_size]
    test_data = data[train_size:]

    # Define the RL model
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=(30,)),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(1)
    ])

    # Train the model using RL
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.01)
    for i in range(100):
        state = train_data[i, :-1]
        action = action_function(model.predict(np.reshape(state, (1, 30))))
        next_state = train_data[i + 1, :-1]
        reward = reward_function(model.predict(np.reshape(state, (1, 30))), train_data[i + 1, -1])
        with tf.GradientTape() as tape:
            predicted_price = model(np.reshape(state, (1, 30)))
            loss = -reward * tf.math.log(predicted_price) if action else -reward * tf.math.log(1 - predicted_price)
        grads = tape.gradient(loss, model.trainable_variables)
        optimizer.apply_gradients(zip(grads, model.trainable_variables))

    # Evaluate the model
    mse = model.evaluate(test_data[:, :-1], test_data[:, -1])
    rmse = sqrt(mse)

    # Make predictions
    last_30_days = test_data[-30:, :-1]
    last_30_days = np.reshape(last_30_days, (1, 30))
    next_day_price = model.predict(last_30_days)
    next_day_price = scaler.inverse_transform(np.concatenate((last_30_days, next_day_price), axis=1))[:, -1]

    # Print the RMSE and next day price
    print('RMSE:', rmse)
    print('Next day price:', next_day_price)


    x = 1




# Define the reward function
def reward_function(predicted_price, actual_price):
    return np.log(predicted_price/actual_price)

# Define the action function
def action_function(prediction):
    return prediction > 0.5
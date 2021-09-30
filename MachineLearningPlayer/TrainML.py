#!/usr/bin/python3

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.models import load_model
import keras.backend as K
    
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error as mse

import matplotlib.pyplot as plt

import os
os.environ['CUDA_VISIBLE_DEVICES'] = '1'  # Random device so tensorflow doesn't use the GPU

if __name__ == "__main__":
    filename = '../count_list_for_ml.csv'

    df = pd.read_csv(filename)
    #row_count = len(df.index)
    #if row_count < 10000:
    #    fraction_to_sample = 1
    #else:
    #    fraction_to_sample = 10000 / row_count

    fraction_to_sample = 1
    df = df.sample(frac=fraction_to_sample).reset_index(drop=True)
    all_X = df[['card2', 'card3', 'card4', 'card5', 'card6', 'card7', 'card8', 'card9', 'card10', 'card11']]
    all_y = df['f_count']

    all_X = np.array(all_X)[:, None]
    X_train, X_test, y_train, y_test = train_test_split(all_X, all_y, shuffle=True, test_size=0.3)

    y_test = np.array(y_test)

    K.clear_session()

    model = Sequential()
    model.add(LSTM(20, return_sequences=False, input_shape=(1, 10)))
    model.add(Dense(1, ))
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['acc', 'mae', 'mape'])

    model.summary()

    early_stop = [EarlyStopping(monitor='val_loss', patience=2, verbose=1), ModelCheckpoint(filepath='./machinelearningplayer.h5', monitor='val_loss', save_best_only=True)]

    history = model.fit(X_train, y_train, validation_split=0.3, batch_size=1, epochs=100, callbacks=early_stop)

    K.clear_session()
    model = load_model('./machinelearningplayer.h5')

    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    print("The MSE on the Train set is:\t{:0.1f}".format(mse(y_train, y_train_pred)))
    print("The MSE on the Test set is:\t{:0.1f}".format(mse(y_test, y_test_pred)))

    print("The R2 score on the Train set is:\t{:0.3f}".format(r2_score(y_train, y_train_pred)))
    print("The R2 score on the Test set is:\t{:0.3f}".format(r2_score(y_test, y_test_pred)))

    #model.save('machinelearningplayer.h5')



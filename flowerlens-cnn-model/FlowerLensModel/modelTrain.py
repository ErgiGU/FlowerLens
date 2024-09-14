# import libraries 
import numpy as np
import os
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.optimizers import Adam

def createModel(dataSplit, VersionName):
    X_train, y_train, X_validate, X_test, y_validate, y_test = dataSplit
    X_train = np.array(X_train)
    y_train = np.array(y_train)
    X_validate = np.array(X_validate)
    y_validate = np.array(y_validate)
    X_test = np.array(X_test)
    y_test = np.array(y_test) 

    model = Sequential()


    # Convolutional layer with more filters, kernel size (3x3), and 'same' padding
    model.add(Conv2D(32, (3, 3), activation='relu', name='conv1', input_shape=(256, 256, 3)))
    model.add(MaxPooling2D((4, 4)))
    model.add(Dropout(0.25))


    # Another convolutional layer with increased filters
    model.add(Conv2D(64, (3, 3), activation='relu', name='conv2'))
    model.add(MaxPooling2D((2, 2)))
    model.add(Dropout(0.25))


    model.add(Conv2D(64, (3, 3), activation='relu', name='conv3'))
    model.add(MaxPooling2D((2, 2)))
    model.add(Dropout(0.25))


    # Flattening
    model.add(Flatten())


    # Dense layer with more units
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.5))  # Dropout for regularization


    # Output layer with softmax activation
    model.add(Dense(11, activation='softmax')) # TODO: change to 16 when want to incorporate all flower classes  


    # Compile the model
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    # Add Early Stopping
    early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5)

    # Print the model summary to see the architecture
    model.summary()

    epochs = 20  # Number of training epochs
    batch_size = 32  # Number of samples per gradient update

    # Fit the model
    history = model.fit(
        X_train, y_train,
        epochs=epochs,
        steps_per_epoch=10,
        verbose=1,
        validation_data=(X_validate, y_validate),
        callbacks=[early_stopping]
    )

    # Evaluate the model on the test data
    test_loss, test_accuracy = model.evaluate(X_test, y_test)

    # Save the model
    current_directory = os.path.dirname(os.path.abspath(__file__))
    path  = os.path.join(current_directory ,'ml_models', 'flower_model_' + VersionName + '.keras' )
    model.save(path)

    return path, test_accuracy


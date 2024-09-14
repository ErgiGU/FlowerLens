import base64
import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from keras.models import load_model
from sklearn.metrics import confusion_matrix, classification_report
import os
import io
import matplotlib.pyplot as plt

# function to produce a performance report out of a model
def performance(modelVersion, X_test, y_test):

    # get model path
    current_directory = os.path.dirname(os.path.abspath(__file__))
    path  = os.path.join(current_directory ,'ml_models', 'flower_model_' + modelVersion + '.keras' )

    # load model
    model = load_model(path)

    # Get the model predictions
    probabilities = model.predict(X_test)
    y_pred = np.argmax(probabilities, axis=1)  # converting probabilities to class labels

    # Compute confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    
    # produce a heatmap
    sns.heatmap(cm, annot=True, fmt='d')
    plt.xlabel('Predicted')
    plt.ylabel('Truth')
    
    # Save the image as a byte stream
    plt.savefig("FlowerLensModel/cm.png")
    #plt.show()

    # Close the plot to avoid memory leaks
    #plt.close()

    # create classification_report
    num_classes = 11
    target_names = ["Class {}".format(i) for i in range(num_classes)]
    print("y_test shape:", y_test.shape)
    print("y_pred shape:", y_pred.shape)

    performance = classification_report(y_test, y_pred, target_names = target_names)
    return performance

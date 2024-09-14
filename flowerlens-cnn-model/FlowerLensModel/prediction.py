from keras.models import load_model
from matplotlib import pyplot as plt
import tensorflow as tf
import numpy as np
import matplotlib.image as mpimg
import os
from tensorflow.keras import backend as K
from scipy import ndimage

# funtion to turn image pixel data from RBG to greyscale (unused as our latest model uses color)
def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])

# function to load a model and make a prediction with an image
def makePrediction(ModelVersion, input):
    # get model path and load it
    current_directory = os.path.dirname(os.path.abspath(__file__))
    path  = os.path.join(current_directory ,'ml_models', 'flower_model_' + ModelVersion + '.keras' )
    print(path)
    MLmodel = load_model(path)

    # Load the image using matplotlib.image
    image = mpimg.imread(input)
    
    # Resize the image to the desired dimensions (e.g., 256x256)
    resized_img = tf.image.resize(image, (256, 256))
    
    # Normalize the pixel values to the range [0, 1]
    normalized_image = resized_img / 255.0
    
    # Add batch dimension to match the expected input shape for CNN
    reshaped_image = tf.expand_dims(normalized_image, axis=0)

    # get prediction
    predictions = MLmodel.predict(reshaped_image)

    # get index of predicted flower
    predicted_class_index = np.argmax(predictions)

    # get flower based on index
    flower = getFlower(predicted_class_index)

    # Get max predicted confidence
    prediction_confidence = np.max(predictions)

    # create heatmap image for explainable AI
    generate_grad_cam(MLmodel, reshaped_image, predicted_class_index)

    # Return tuple (flower, prediction_accuracy)
    return flower, prediction_confidence

# Function to generate the advanced AI functionality (prediction heatmap)
def generate_grad_cam(model, image, class_index):
    
    # get output of last convolutional layer
    last_conv_layer = model.get_layer('conv3')
    heatmap_model = tf.keras.models.Model([model.inputs], [last_conv_layer.output, model.output])

    # generate heatmap with image and last convolutional layer
    with tf.GradientTape() as tape:
        conv_output, predictions = heatmap_model(image)
        loss = predictions[:, class_index]

    grads = tape.gradient(loss, conv_output)
    pooled_grads = K.mean(grads, axis=(0, 1, 2))
    heatmap = tf.reduce_mean(tf.multiply(conv_output, grads), axis=-1)

    heatmap = np.squeeze(heatmap)
    heatmap = np.maximum(heatmap, 0)
    heatmap /= np.max(heatmap)

    # Upsample the heatmap to match the original image size
    upscaled_heatmap = ndimage.zoom(heatmap, zoom=(256 / 39, 256 / 39), order=1)

    # Overlay the heatmap onto the original image
    alpha = 0.6  # Set the transparency of the heatmap
    reshaped_image = np.squeeze(image)
    plt.imshow(reshaped_image)
    plt.imshow(upscaled_heatmap, cmap='jet', alpha=alpha)  # Use 'jet' colormap for heatmap visualization
    plt.axis('off')
    plt.savefig('FlowerLensModel/heatmap.png', bbox_inches='tight', pad_inches=0)  # Save as an image
    plt.show()

    # Close the plot to avoid memory leaks
    plt.close()

# function to match numeric class value to its string name (EG. 0 to rose)
def getFlower(input):
    flower = ""
    match input:
        case 0:
            flower="rose"
        case 1:
            flower="sunflower"
        case 2:
            flower="bellflower"
        case 3:
            flower="common_daisy"
        case 4:
            flower="daffodil"
        case 5:
            flower="dandelion"
        case 6:
            flower="iris"
        case 7:
            flower="california_poppy"
        case 8:
            flower="tulip"
        case 9: 
            flower="carnation"
        case 10: 
            flower="astilbe"
        case 11: 
            flower="black_eyed_susan" 
        case 12: 
            flower="coreopsis" 
        case 13: 
            flower="calendula"
        case 14: 
            flower="magnolia"
        case 15: 
            flower="water_lily"
        case _:
            print("Error, case wasn't 0-9")   
    return flower
    



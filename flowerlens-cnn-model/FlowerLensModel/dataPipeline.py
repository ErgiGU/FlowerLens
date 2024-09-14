# import libraries 
import pandas as pd # Import Pandas for data manipulation using dataframes
import numpy as np # Import Numpy for data statistical analysis 
import matplotlib.pyplot as plt # Import matplotlib for data visualisation
import seaborn as sns
import matplotlib.image as mpimg
import csv
import os
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])

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

def getTrainingData():

    current_directory = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = current_directory + "/output/flowers.csv"
    with open(csv_file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Class'.format(0)]+['Pixel{}'.format(i+1) for i in range(196608)])
        
        for flowerClass in range (11):
            flower = getFlower(flowerClass)
            
            # Path to the folder containing JPEG images
            current_directory = os.path.dirname(os.path.abspath(__file__))
            current_flower_path = current_directory + "/input/" + flower
            #for debugging
            print(current_flower_path)
            
            # Get a list of all files in the folder
            files = os.listdir(current_flower_path)
            
            # Filter only JPEG files
            jpg_files = [file for file in files if file.lower().endswith(".jpg")]
            
            # Loop through each JPEG file
            for jpg_file in jpg_files:
                
                # Construct the full file path
                file_path = os.path.join(current_flower_path, jpg_file)
                
                # Open the image
                img = mpimg.imread(file_path)

                # Resize the image
                resized_img = tf.image.resize(img, (256, 256)).numpy()
                
                # Flatten the NumPy array
                pixel_values = resized_img.flatten().tolist()

                csv_writer.writerow([flowerClass] + pixel_values)
                
    return csv_file_path

def splitData():
    # Code below inspired by https://datascience.stackexchange.com/a/53161
    # ratios for the different datasets
    train_ratio = 0.60
    validation_ratio = 0.20
    test_ratio = 0.20

    if (train_ratio + validation_ratio + test_ratio != 1):
        print("Error, change dataset ratio so that they add up to 1")
    else:
        # Load csvs as training data
        current_directory = os.path.dirname(os.path.abspath(__file__))
        csv_file_path = current_directory + "/output/flowers.csv"

        flower_train_df = pd.read_csv(csv_file_path,sep=',')
        flower_training = np.array(flower_train_df, dtype = 'int')

        # Prepare the training and testing dataset 
        X_train = flower_training[:,1:]/255
        y_train = flower_training[:,0]
        # This gives us the traning set
        X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size=1 - train_ratio)

        # This gives us the validation and testing sets
        X_validate, X_test, y_validate, y_test = train_test_split(X_test, y_test, test_size=test_ratio/(test_ratio + validation_ratio)) 
        print("Original shape:", X_train.shape)
        print("Original size:", X_train.size)
        # unpack the tuple. Reshape the data in a form that CNN can accept 
        X_train = X_train.reshape(X_train.shape[0], *(256, 256, 3))
        X_test = X_test.reshape(X_test.shape[0], *(256, 256, 3))
        X_validate = X_validate.reshape(X_validate.shape[0], *(256, 256, 3))
        print("done!")

        dataSplit = (X_train, y_train, X_validate, X_test, y_validate, y_test)

    return dataSplit

def DirectImageDataSplit():
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Create an empty DataFrame with columns for flowerClass and individual pixels
    df_columns = ["flowerClass"] + [f"Pixel{i}" for i in range(256 * 256 * 3)]  # Assuming images are RGB with size 256x256
    flower_train_df = pd.DataFrame(columns=df_columns)

    for flowerClass in range(14):  # TODO: change to 16 when you want to incorporate all flower classes
        flower = getFlower(flowerClass)

        # Path to the folder containing JPEG images
        current_flower_path = os.path.join(current_directory, "input", flower)
        print("reading:", current_flower_path)

        # Get a list of all files in the folder
        files = os.listdir(current_flower_path)

        # Filter only JPEG files
        jpg_files = [file for file in files if file.lower().endswith(".jpg")]

        # Loop through each JPEG file
        for jpg_file in jpg_files:
            file_path = os.path.join(current_flower_path, jpg_file)
            print(file_path)
            print(1)

            # Open and resize the image using TensorFlow
            img = tf.io.read_file(file_path)
            img = tf.image.decode_jpeg(img, channels=3)  # Assuming RGB images
            resized_img = tf.image.resize(img, (256, 256))

            # Flatten the TensorFlow tensor
            pixel_values = tf.reshape(resized_img, [-1]).numpy()

            # Append a row to the DataFrame
            list_row = [str(flowerClass)] + pixel_values.tolist()
            flower_train_df.loc[len(flower_train_df)] = list_row

    # Perform the data split
    train_ratio = 0.60
    validation_ratio = 0.20
    test_ratio = 0.20

    if train_ratio + validation_ratio + test_ratio != 1:
        print("Error, change dataset ratio so that they add up to 1")
    else:
        flower_training = np.array(flower_train_df["pixelData"].tolist(), dtype='int')
        flower_labels = np.array(flower_train_df["flowerClass"].tolist(), dtype='int')

        X_train, X_temp, y_train, y_temp = train_test_split(
            flower_training, flower_labels, test_size=1 - train_ratio)

        X_validate, X_test, y_validate, y_test = train_test_split(
            X_temp, y_temp, test_size=test_ratio / (test_ratio + validation_ratio))

        print("Original shape:", X_train.shape)
        print("Original size:", X_train.size)

        # Reshape the data in a form that CNN can accept
        X_train = X_train.reshape(X_train.shape[0], 256, 256, 3)
        X_test = X_test.reshape(X_test.shape[0], 256, 256, 3)
        X_validate = X_validate.reshape(X_validate.shape[0], 256, 256, 3)

        print("done!")

        dataSplit = (X_train, y_train, X_validate, X_test, y_validate, y_test)

    return dataSplit
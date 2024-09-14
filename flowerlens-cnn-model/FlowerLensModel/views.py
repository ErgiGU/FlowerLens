import base64
import threading
import requests
import os
import csv
from django.http import FileResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .dataPipeline import getTrainingData
from .dataPipeline import splitData
from .modelTrain import createModel
from .performance import performance
from .prediction import makePrediction
from .serializers import TrainFlowerSerializer, ImageSerializer
from .models import TrainFlower, Images
from django.conf import settings
from rest_framework import generics
from .dataPipeline import getFlower
import shutil


# initial message to confirm connection
def home(request):
    return HttpResponse("FlowerLensModel is now online")

# API endpoints
@api_view(['POST', 'PUT', 'DELETE', 'GET'])
def pipe_filter(request): # this handles HHTP request
    """Filter Function"""
    message = request.data.get('topic')
    print(message)
    match message:
        
        # if message is train model 
        case "trainModel":

            # execute model training
            thread = threading.Thread(target=trainModel, args=(request,))
            thread.start()
            
            # Response that says the model has started training
            return Response({'message': 'request recieved, model has started training'},status = 200)

        # if message is predict
        case "predict":
            # make the prediction
            response, status = predict(request)
            return Response(response)
        
        # if message is invalid, notify backend
        case _:
            return Response({'error': 'Invalid command'}, status=400)
    
# function that checks the request validity and executes prediction functions
def predict(request):
    # read model version used for prediction
    #uploaded_image = request.get('image')
    version = request.data.get('version')
    if version == None:
        message = {'error': 'Did not get a model version in the request'}
        status = 500
        return message, status

    # read image
    if 'image' not in request.FILES:
        message = {'error': 'Image file is missing in the request'}
        status = 500  
        return message, status
    image_file = request.FILES['image']

    # make prediction
    flower, prediction_confidence = makePrediction(version, image_file)
    #current_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)) , "test_flower.jpg")
    #with open(current_directory, 'rb') as file:
    #    heatmap = image_file.read()
    heatmap = image_file.read()
    if flower is None or prediction_confidence is None or heatmap is None:
        message = {'error': 'there was a problem generating a prediction'}
        status = 500  
        return message, status
    
    # if everything works, send 200 and return prediction, confidence, heatmap
    current_directory = os.path.dirname(os.path.abspath(__file__))
    path  = os.path.join(current_directory ,'heatmap.png')
    with open(path, 'rb') as img_file:
        encoded_image = base64.b64encode(img_file.read()).decode('utf-8')
    data = {
    "prediction": flower,
    "confidence": str(prediction_confidence),
    "heatmap": encoded_image
    }

    status = 200
    return data, status

# function that checks the request validity and executes the model training functions
def trainModel(request):
    # read model version to name the new model
    version = request.data.get('version')
    model_id = request.data.get('model_id')


    if version is None or len(version) == 0:
        message = {'error': 'Version/model_id is either None or an empty string'}
        status = 500
        return message, status

    # get path for input folder
    current_directory = os.path.dirname(os.path.abspath(__file__))
    input_path  = os.path.join(current_directory ,'input')

    # delete content inside input folder (old training data)
    try:
        shutil.rmtree(input_path)
        os.makedirs(input_path)
    except Exception as e:
        message = {'error': f'Failed to clear input folder: {str(e)}'}
        status = 500
        return message, status
    
    # function to pull all training data from the DB
    for i in range (11):
        flower = getFlower(i)
        pullAllImages(flower)

    # get training data
    data = getTrainingData()
    split_data = splitData()
    if split_data == None:
        message = {'error': 'Data could not be split'}
        status = 500
        return message, status

    _, _, _, X_test, _, y_test = split_data

    # train model
    model, test_accuracy = createModel(split_data, version)
    if not os.path.exists(model):
        message = {'error': 'Model could not be trained'}
        status = 500
        return message, status

    # generate performance metrics, generate confusion matrix
    performance_analysis = performance(version, X_test, y_test)

    if performance_analysis == None:
        message = {'error': 'Performance metrics or confusion_matrix could not be generated'}
        status = 500
        return message, status
    
    # If everything works, send 200, performance and confusion matrix
    current_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)) , "cm.png")
    with open(current_directory, 'rb') as file:
        confusion_matrix = file.read()
    if performance_analysis != None:
        data = {'topic': 'trainedModel',
                "model_id": model_id,
                'version': version,
                "test_accuracy": test_accuracy,
                'performance_analysis': performance_analysis,
            }
        files = {
            'confusion_matrix': confusion_matrix
        }
        status = 200
        url = 'http://127.0.0.1:8000/trainedModel/'
        requests.post(url, files=files, data=data)
    else: #TODO: maybe change this
        message = {'error': 'Unkown error'}
        status = 500
        return message, status

def pullAllImages(flower_class):
    print(flower_class)
    # query all flowers corresponding to flower class
    queryset = Images.objects.filter(flower=flower_class)

    # serialize data with fields flower(flower class) and image (image file)
    serialized_data = ImageSerializer(queryset, many=True)

    # store data in variable
    images = serialized_data.data

    # Path where flower images are to be stored
    end_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input", flower_class)

    # Create the folder if it doesn't exist
    os.makedirs(end_path, exist_ok=True)

    # Save images one by one to the end_path
    counter = 0
    for image_data in images:
        counter += 1
        image_url = image_data['image']
        image_path = os.path.join(end_path, f"{counter}.jpg")

        # Download the image from the URL
        response = requests.get(image_url)
        if response.status_code == 200:
            # Save the downloaded image to the specified folder
            with open(image_path, 'wb') as dest_file:
                dest_file.write(response.content)
        else:
            print(f"Failed to download image from {image_url}")
import json
from rest_framework.response import Response
import requests
from .models import Photo, AIModel, PredictionResult


def upload_photo(request):
    """Function for uploading photo"""
    if 'photo' in request.FILES:
        photo = request.FILES["photo"]
        # Call cnn_model to process the photo and get prediction
        prediction, confidence, heatmap = cnn_model(photo)
        # Create a new instance of the model
        new_photo = Photo()
        # Assign the uploaded file to the ImageField
        new_photo.image = photo
        new_photo.title = prediction
        new_photo.description = (f"Condifidence being a {prediction} is {confidence}%")
        # Save the model instance, not the ImageField
        new_photo.save()
        
        flower_json_files = {
            "astilbe": "FlowerLensBackend/flowerInfoJSONs/astilbe.json",
            "bellflower": "FlowerLensBackend/flowerInfoJSONs/bellflower.json",
            "black_eyed_susan": "FlowerLensBackend/flowerInfoJSONs/black_eyed_susan.json",
            "calendula": "FlowerLensBackend/flowerInfoJSONs/calendula.json",
            "california_poppy": "FlowerLensBackend/flowerInfoJSONs/california_poppy.json",
            "carnation": "FlowerLensBackend/flowerInfoJSONs/carnation.json",
            "common_daisy": "FlowerLensBackend/flowerInfoJSONs/common_daisy.json",
            "daffodil": "FlowerLensBackend/flowerInfoJSONs/daffodil.json",
            "dandelion": "FlowerLensBackend/flowerInfoJSONs/dandelion.json",
            "iris": "FlowerLensBackend/flowerInfoJSONs/iris.json",
            "magnolia": "FlowerLensBackend/flowerInfoJSONs/magnolia.json",
            "rose": "FlowerLensBackend/flowerInfoJSONs/rose.json",
            "sunflower": "FlowerLensBackend/flowerInfoJSONs/sunflower.json",
            "tulip": "FlowerLensBackend/flowerInfoJSONs/tulip.json",
            "water_lily": "FlowerInfoJSONs/water_lily.json",  
        }
        
        # Determine which JSON file to use based on the prediction
        json_file_name = flower_json_files.get(prediction)

        # Load the appropriate JSON data
        if json_file_name:
            with open(json_file_name, 'r') as file:
                flower_info = json.load(file)
        else:
                flower_info = "No additional information available"
        # Create response data
        response_data = {
            "prediction": prediction,
            "confidence": confidence,
            "heatmap": heatmap,
            "flowerInfo": flower_info,
            "message": "uploadPhoto"
        }

        return Response(response_data, status=200)
    else:
        return Response({'error': 'No photo uploaded'}, status=400)


def cnn_model(photo):
    """
    Send the image to the CNN service and get back the prediction,
    confidence, and heatmap. Requires the photo file and model version.
    """
    # API endpoint for the CNN model prediction service
    image = photo.open().read()
    cnn_service_endpoint = 'http://flowerlens-cnn-service:80/predict/'
    
    # Find the deployed version, using the is_deployed version
    latest_model = AIModel.objects.filter(is_deployed = True).first()
    if latest_model:
        model_version = latest_model.version
    else:
        model_version = 'v.1'  # Or handle the case where no version is available

    # Read the image file
    data = {"topic": "predict",
            "version": model_version,}
    message = {
        "image": image,
    }

    print("Hello")

    response = requests.post(cnn_service_endpoint, files=message, data=data)

    print("Response: ", response)

    # If the request is successful, parse the prediction results
    if response.status_code == 200 and response.text:
        result = response.json()
        prediction = result.get('prediction')
        confidence = result.get('confidence')
        heatmap = result.get("heatmap")

        # Save the results in the database
        prediction_result = PredictionResult(
            prediction=prediction,
            confidence=confidence,
        )
        prediction_result.save()

    else:
        # Handle the error case appropriately
        prediction = None
        confidence = None
        heatmap = None

    return prediction, confidence, heatmap

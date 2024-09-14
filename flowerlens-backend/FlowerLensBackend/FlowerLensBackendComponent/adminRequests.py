from rest_framework.response import Response
import requests
from django.http import JsonResponse
from .serializers import AIModelSerializer, MetricsTableSerializer, MatrixImageSerializer
from .models import AIModel, MetricsTable, MatrixImage
from django.db.models import Max
from django.db import transaction


def list_ai_models():
    """Function for fetching all AI models except the one that is deployed."""
    
    # Fetch all AIModel instances except the one that is currently deployed
    queryset = AIModel.objects.filter(is_deployed=False)
    
    # Serialize the queryset
    serializer = AIModelSerializer(queryset, many=True)
    
    # Return the serialized data as a JSON response
    return JsonResponse(serializer.data, safe=False)


def current_evaluation():
    """Function for fetching the current evaluation data for the deployed model."""
    # Get the deployed AIModel instance
    deployed_model = AIModel.objects.filter(is_deployed=True).first()

    if deployed_model:
        # Fetch MetricsTable instances associated with the deployed AIModel
        metrics_queryset = MetricsTable.objects.filter(model_id=deployed_model)
        # Fetch MatrixImage instances associated with the deployed AIModel
        matrix_images_queryset = MatrixImage.objects.filter(model_id=deployed_model)

        # Serialize the querysets
        metrics_serializer = MetricsTableSerializer(metrics_queryset, many=True)
        matrix_images_serializer = MatrixImageSerializer(matrix_images_queryset, many=True)

        # Prepare the response data
        response_data = {
            'version': deployed_model.version,
            'metrics': metrics_serializer.data,
            'matrix_images': matrix_images_serializer.data
        }

        # Return the serialized data as a JSON response
        return JsonResponse(response_data, safe=False)
    else:
        # Handle the case where no deployed AI model is found
        return JsonResponse({'error': 'No deployed AI model found'}, status=404)

def generate_version():
    """Generate a new version number with 'v.' prefix."""
    max_version = AIModel.objects.aggregate(Max('version'))['version__max']
    if max_version:
        max_version_number = int(max_version.split('.')[1])
        new_version_number = max_version_number + 1
    else:
        new_version_number = 1
    return f'v.{new_version_number}'


def generate_model_id():
    """Generate a unique model ID."""
    max_id = AIModel.objects.aggregate(Max('model_id'))['model_id__max']
    if max_id:
        new_id = int(max_id) + 1
    else:
        new_id = 1
    return str(new_id)

def train_ai_model(request):
    """Function for training AI model."""
    
    cnn_model_url = 'http://34.32.204.245:8001/trainModel/'

    # Generate new model_id and version
    model_id = generate_model_id()
    version = generate_version()

    try:
        payload = {
            'model_id': model_id,
            'version': version,
            'topic': 'trainModel'
        }

        # Send a POST request to start training the model
        response = requests.post(cnn_model_url, json=payload)

        if response.status_code == 200:
            print("Training started successfully, check in 20 mins")
            return JsonResponse({'message': 'Training started successfully', 'model_id': model_id, 'version': version}, status=200)
        else:
            print("Failed to start training")
            return JsonResponse({'error': 'Failed to start training'}, status=response.status_code)
    except requests.exceptions.RequestException as e:
        print(f"Error sending request to CNN model server: {e}")
        return JsonResponse({'error': str(e)}, status=500)



def evaluate_ai_model(request):
    """Function for evaluating AI model"""
    model_version = request.data.get('version')

    # Fetch AIModel instance based on version
    try:
        ai_model = AIModel.objects.get(version=model_version)
    except AIModel.DoesNotExist:
        return Response({'error': 'AI model not found'}, status=404)

    # Fetch MetricsTable instances associated with the AIModel
    metrics_queryset = MetricsTable.objects.filter(model_id=ai_model)
    matrix_images_queryset = MatrixImage.objects.filter(model_id=ai_model)

    # Serialize the querysets
    metrics_serializer = MetricsTableSerializer(metrics_queryset, many=True)
    matrix_images_serializer = MatrixImageSerializer(matrix_images_queryset, many=True)

    # Prepare the response data
    response_data = {
        'metrics': metrics_serializer.data,
        'matrix': matrix_images_serializer.data
    }

    # Return the serialized data as a JSON response
    return Response(response_data, status=200)


def deploy_model(request):
    """Function for deploying AI model."""
    version = request.data.get('version')
    if version is None:
        return Response({'error': 'Version is required'}, status=400)

    try:
        with transaction.atomic():
            # Set all models' is_deployed and latest_deployed to False
            AIModel.objects.update(is_deployed=False, latest_deployed=False)

            # Set the specified model's is_deployed to True
            model_to_deploy = AIModel.objects.get(version=version)
            model_to_deploy.is_deployed = True
            model_to_deploy.latest_deployed = True
            model_to_deploy.save()

        return Response({'message': 'Model deployed successfully'})

    except AIModel.DoesNotExist:
        return Response({'error': 'AI Model not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


def rollback_model():
    """Function to delete the latest non-deployed AI model from the database."""

    try:
        with transaction.atomic():
            model_to_rollback = AIModel.objects.get(is_deployed=True, latest_deployed=False)
            deployed_version = model_to_rollback.version

            # Delete related records
            MetricsTable.objects.filter(model_id=model_to_rollback).delete()
            MatrixImage.objects.filter(model_id=model_to_rollback).delete()

            # Delete the model
            model_to_rollback.delete()

            # Activate the latest deployed model
            current_model = AIModel.objects.get(latest_deployed=True)
            current_model.is_deployed = True
            current_model.save()

            return JsonResponse({'message': f'AI model successfully rolled back, old version {deployed_version} is being used'}, status=200)

    except AIModel.DoesNotExist:
        return JsonResponse({'message': 'Train an AI Model first'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)




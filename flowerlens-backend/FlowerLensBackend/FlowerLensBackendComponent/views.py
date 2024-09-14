from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from FlowerLensBackendComponent.uploadPhoto import upload_photo
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .adminRequests import list_ai_models, train_ai_model, evaluate_ai_model, current_evaluation, rollback_model, deploy_model
from .modelRequests import save_model
from .uploadPhoto import upload_photo


# USER FUNCTIONS

def home(request):
    """Landing page message"""
    return HttpResponse("Welcome to FlowerLensBackend! The backend is up and running.")

# User pipe-filter, check incoming topics and filter accordingly.
@api_view(['POST', 'PUT', 'DELETE', 'GET'])
def pipe_filter_user(request):
    """Filer Function"""
    message = request.data.get('topic')

    if message == 'uploadPhoto':
        return upload_photo(request)
    else:
        # You should return an appropriate HTTP response for every possible code path
        return Response({'error': 'Invalid command'}, status=400)

# ADMIN VIEWS

# Admin pipe-filter, check incoming topics and filter accordingly.
# fetch AI model, retrain AI model, evaluate AI model, fetch confusion matrix, fetch metrics, deploy AI model, rollback AI model.
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def pipe_filter_admin(request):
    """ Admin pipe filter architecture """
    message = request.data.get('topic')
    if message == 'listModels':
        respond = list_ai_models()
    elif message == 'trainModel':
        respond = train_ai_model(request)
    elif message == 'evaluateVersion':
        respond = evaluate_ai_model(request)
    elif message == "currentEvaluation":
        respond = current_evaluation()
    elif message == "rollbackModel":
        respond = rollback_model()
    elif message == "deployModel":
        respond = deploy_model(request)
    else:
        respond = Response({'error': 'Invalid command'}, status=400)
    return respond


## AI Model CNN pipe-filter, check incoming topics and filter accordingly.
# save model, fetch trained model
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def cnn_model_pipefilter(request):
    """ CNN model pipe filter architecture """
    message = request.data.get('topic')
    if message == 'trainedModel':
        respond = save_model(request)
    else:
        respond = Response({'error': 'Invalid command'}, status=400)
    return respond


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    """Login view for the admin user"""

    def post(self, request, *args, **kwargs):
        """Login the admin user and return JWT tokens"""
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # User is authenticated, create and return JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        
        # Authentication failed
        return Response({'detail': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

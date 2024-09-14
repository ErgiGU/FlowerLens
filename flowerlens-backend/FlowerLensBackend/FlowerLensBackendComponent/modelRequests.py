import re
from django.http import JsonResponse
from django.utils import timezone
from .models import AIModel, MetricsTable, MatrixImage


def extract_metrics(performance_analysis):
    """Function for extracting weighted avg precision, recall, f1-score from the performance analysis."""
    # Search for the weighted avg values
    weighted_avg_match = re.search(r'weighted avg\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)', performance_analysis)
    
    if weighted_avg_match:
        precision = float(weighted_avg_match.group(1))
        recall = float(weighted_avg_match.group(2))
        f1_score = float(weighted_avg_match.group(3))
    else:
        precision, recall, f1_score = None, None, None

    # Return a dictionary with the extracted metrics
    return {
        'precision': precision,
        'recall': recall,
        'f1_score': f1_score
    }


def save_model(request):
    """Function for saving AI model with associated metrics and confusion matrix."""
    # Check for required fields
    required_fields = ['model_id', 'version', 'performance_analysis', 'confusion_matrix']
    if not all(field in request.data for field in required_fields):
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    # Extract data from request
    model_id = request.data.get('model_id', '1')
    model_version = request.data['version']
    test_accuracy = request.data.get('test_accuracy')  # Extracting test_accuracy
    performance_analysis = request.data['performance_analysis']
    confusion_matrix = request.FILES.get("confusion_matrix")

    # Extract metrics from performance analysis
    extracted_metrics = extract_metrics(performance_analysis)
    AIModel.objects.update(is_deployed=False)

    try:
        # Create and save the new AIModel instance
        ai_model = AIModel(
            model_id=model_id,
            version=model_version,
            timestamp=timezone.now()
        )
        ai_model.is_deployed = True
        ai_model.full_clean()  # Validate the model instance
        ai_model.save()

        # Create and save the MetricsTable instance
        metrics_table = MetricsTable(
            model_id=ai_model,
            accuracy=test_accuracy,  # Using test_accuracy for accuracy
            precision=extracted_metrics.get('precision', 0),
            recall=extracted_metrics.get('recall', 0),
            f1_score=extracted_metrics.get('f1_score', 0),
            timestamp=timezone.now()
        )
        
        metrics_table.full_clean()
        metrics_table.save()

        # Handling the Confusion Matrix
        if confusion_matrix:
            # Saving the matrix image information in the database
            matrix_image = MatrixImage(
                model_id=ai_model,
                timestamp=timezone.now()
            )
            matrix_id = "matrix_id_" + str(ai_model.model_id)
            matrix_image.image_path.save(matrix_id +".png", confusion_matrix, save=True)  # Saving the file path instead of the image object
            matrix_image.full_clean()
            matrix_image.save()
        return JsonResponse({'message': 'Model and metrics saved successfully'}, status=201)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

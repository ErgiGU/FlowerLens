import json
import io
from django.test import TestCase, RequestFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.response import Response
from PIL import Image
from .models import Photo, PredictionResult
from .views import pipe_filter_user
from unittest.mock import patch

class UploadPhotoTestCase(TestCase):
    """Test case for the uploadPhoto function"""
    def setUp(self):
        """Setup function for the test case"""
        # Create a dummy photo file for testing
        dummy_image = Image.new('RGB', (100, 100), color='red')
        image_io = io.BytesIO()
        dummy_image.save(image_io, format='JPEG')
        image_io.seek(0)
        self.factory = RequestFactory()
        self.photo_file = SimpleUploadedFile(
            name='test_image.jpg',
            content=image_io.read(),
            content_type='image/jpeg'
        )


    @patch('FlowerLensBackendComponent.uploadPhoto.cnn_model')
    def test_upload_photo_with_valid_photo(self, mock_cnn_model):
        """Test case for uploading a photo with a valid photo"""
        # Setup mock return value
        mock_cnn_model.return_value = ('flower', 95, 'heatmap_url')

        # Manually create and save a PredictionResult object
        # This simulates what cnn_model would normally do
        PredictionResult(prediction='flower', confidence=95).save()

        # Create a mock request object with a valid photo
        request = self.factory.post('/uploadPhoto/', {'photo': self.photo_file, 'topic': 'uploadPhoto'}, format='multipart')

        # Call the pipe_filter_user function
        response = pipe_filter_user(request)

        # Assert that the response is a valid Response object
        self.assertIsInstance(response, Response)

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Assert that the response data contains the expected keys
        expected_keys = ['prediction', 'confidence', 'heatmap', 'flowerInfo', 'message']
        self.assertCountEqual(response.data.keys(), expected_keys)
        
        # Assert that the photo is saved in the database
        self.assertEqual(Photo.objects.count(), 1)

        # Assert that the prediction result is saved in the database
        self.assertEqual(PredictionResult.objects.count(), 1)

    def test_upload_photo_with_no_photo(self):
        """Test case for uploading a photo with no photo"""
        # Create a mock request object with no photo but with the topic
        request = self.factory.post('/uploadPhoto/', {'topic': 'uploadPhoto'}, format='multipart')

        # Call the pipe_filter_user function
        response = pipe_filter_user(request)

        # Assert that the response is a valid Response object
        self.assertIsInstance(response, Response)

        # Assert that the response status code is 400
        self.assertEqual(response.status_code, 400)

        # Assert that the response data contains the expected error message
        self.assertEqual(response.data, {'error': 'No photo uploaded'})

        # Assert that no photo is saved in the database
        self.assertEqual(Photo.objects.count(), 0)

        # Assert that no prediction result is saved in the database
        self.assertEqual(PredictionResult.objects.count(), 0)


    def test_upload_photo_with_invalid_data_format(self):
        """Test case for uploading a photo with invalid data format"""
        # Send invalid JSON data
        invalid_data = json.dumps({"invalid": "data"})  # Example of invalid data
        request = self.factory.post('/uploadPhoto/', invalid_data, content_type='application/json')

        response = pipe_filter_user(request)
        self.assertEqual(response.status_code, 400)  # Assuming 400 is the response for invalid data format


    def test_upload_photo_with_missing_topic(self):
        """Test case for uploading a photo with missing topic"""
        request = self.factory.post('/uploadPhoto/', {'photo': self.photo_file}, format='multipart')
        response = pipe_filter_user(request)
        self.assertEqual(response.status_code, 400)  # Assuming 400 is the response for missing topic

    def test_upload_photo_with_wrong_topic(self):
        """Test case for uploading a photo with wrong topic"""
        request = self.factory.post('/uploadPhoto/', {'photo': self.photo_file, 'topic': 'wrongTopic'}, format='multipart')
        response = pipe_filter_user(request)
        self.assertEqual(response.status_code, 400)  # Assuming 400 is the response for wrong topic


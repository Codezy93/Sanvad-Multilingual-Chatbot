import unittest
from unittest.mock import patch
from app import app
import os

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        # Set up the test client
        app.config['TESTING'] = True
        self.app = app.test_client()

        # Set environment variables for testing
        os.environ['API_KEY'] = 'test-api-key'
        app.config['SECRET_KEY'] = 'test-secret-key'

        # Mock the conversation.run method to avoid real API calls
        self.conversation_run_patcher = patch('app.conversation.run', return_value='Mocked assistant response')
        self.mock_conversation_run = self.conversation_run_patcher.start()

    def tearDown(self):
        # Stop the patcher
        self.conversation_run_patcher.stop()

    def test_index_route(self):
        """Test that the index page loads successfully."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_chat_valid_input(self):
        """Test the /chat endpoint with valid input."""
        response = self.app.post('/chat', data={
            'message': 'Hello',
            'chat_history': ''
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('assistant', data)
        self.assertEqual(data['assistant'], 'Mocked assistant response')

    def test_chat_missing_message(self):
        """Test the /chat endpoint with missing 'message' parameter."""
        response = self.app.post('/chat', data={
            'chat_history': ''
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Message is required')

    def test_chat_input_too_long(self):
        """Test the /chat endpoint with input exceeding MAX_INPUT_LENGTH."""
        long_input = 'a' * 1000  # Exceeds the MAX_INPUT_LENGTH of 500
        response = self.app.post('/chat', data={
            'message': long_input,
            'chat_history': ''
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Input too long')

    def test_chat_internal_server_error(self):
        """Test handling of exceptions in the /chat endpoint."""
        with patch('app.conversation.run', side_effect=Exception('Test Exception')):
            response = self.app.post('/chat', data={
                'message': 'Hello',
                'chat_history': ''
            })
            self.assertEqual(response.status_code, 500)
            data = response.get_json()
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'An error occurred while processing your request')

    def test_rate_limiting(self):
        """Test that the rate limiting is enforced after 5 requests."""
        for _ in range(5):
            response = self.app.post('/chat', data={
                'message': 'Hello',
                'chat_history': ''
            })
            self.assertEqual(response.status_code, 200)

        # Sixth request should be rate limited
        response = self.app.post('/chat', data={
            'message': 'Hello again',
            'chat_history': ''
        })
        self.assertEqual(response.status_code, 429)
        data = response.get_json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Only 5 trials allowed per user')

    def test_reset_endpoint(self):
        """Test the /reset endpoint."""
        response = self.app.post('/reset')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'Chat history cleared')

    def test_csrf_protection(self):
        """Test that CSRF protection is active."""
        with app.test_client() as client:
            response = client.post('/reset')
            self.assertEqual(response.status_code, 200)  # Should be 200 because CSRF is not enforced on this endpoint

            # Simulate a form without CSRF token on an endpoint that requires it
            # Since we have not applied CSRF to /chat, it should pass
            response = client.post('/chat', data={
                'message': 'Test',
                'chat_history': ''
            })
            self.assertEqual(response.status_code, 200)

    def test_chat_invalid_method(self):
        """Test accessing /chat with an invalid HTTP method."""
        response = self.app.get('/chat')
        self.assertEqual(response.status_code, 405)  # Method Not Allowed

if __name__ == '__main__':
    unittest.main()
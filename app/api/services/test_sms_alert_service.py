import unittest
from unittest.mock import patch
from app.api.services.sms_alert_service import SMSAlertService

class TestSMSAlertService(unittest.TestCase):
    def setUp(self):
        self.username = "test_username"
        self.api_key = "test_api_key"
        self.service = SMSAlertService(self.username, self.api_key)

    @patch('app.api.services.sms_alert_service.africastalking.SMS.send')
    def test_send_sms_success(self, mock_send):
        mock_send.return_value = {"status": "success", "messageId": "12345"}

        phone_number = "+254712345678"
        message = "Hello, this is a test message!"

        self.service.send_sms(phone_number, message)

        mock_send.assert_called_once_with(message, [phone_number])

    @patch('app.api.services.sms_alert_service.africastalking.SMS.send')
    def test_send_sms_failure(self, mock_send):

        mock_send.side_effect = Exception("API Error")

        phone_number = "+254712345678"
        message = "This will fail!"

        with self.assertRaises(Exception) as context:
            self.service.send_sms(phone_number, message)

        self.assertEqual(str(context.exception), "API Error")

if __name__ == '__main__':
    unittest.main()
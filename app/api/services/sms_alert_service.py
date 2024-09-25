import africastalking
import logging

logger = logging.getLogger(__name__)

class SMSAlertService:
    def __init__(self, username: str, api_key: str):
        africastalking.initialize(username, api_key)
        self.sms = africastalking.SMS

    def send_sms(self, phone_number: str, message: str):
        try:
            response = self.sms.send(message, [phone_number])
            logger.info(f"SMS sent successfully to {phone_number}: {response}")
        except Exception as e:
            logger.error(f"Failed to send SMS to {phone_number}: {str(e)}")
            raise e
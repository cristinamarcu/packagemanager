import unittest
import mock
from Config import SMTP_LOGIN, SMTP_PASSWORD
from Notification import build_message, send_notification


class BuildMessageTest(unittest.TestCase):
    def test_msg_format(self):
        # GIVEN
        apartment = "testapartment"
        name = "testname"
        description = "testdescription"
        date = "testdate"
        action = "testaction"

        expected_message = "Hi testname,\nThe package testdescription for apartment testapartment, on testdate was " \
                           "testaction.\nThank you."

        # WHEN
        output_message = build_message(apartment, name, description, date, action)

        # THEN
        self.assertEqual(output_message, expected_message)


class SendNotificationTest(unittest.TestCase):
    @mock.patch("smtplib.SMTP_SSL")
    def test_send_notification(self, mock_SMTP_SSL):
        # GIVEN
        mock_SMTP_SSL_instance = mock_SMTP_SSL.return_value.__enter__.return_value
        email = "testemail"
        apartment = "testapartment"
        name = "testname"
        description = "testdescription"
        date = "testdate"
        action = "testaction"

        # WHEN
        result = send_notification(email, apartment, name, description, date, action)


        # THEN
        mock_SMTP_SSL_instance.login.assert_called_with(SMTP_LOGIN, SMTP_PASSWORD)
        mock_SMTP_SSL_instance.send_message.assert_called()
        self.assertTrue(result)

import unittest
from unittest.mock import patch, MagicMock
import time
from irrigator import RELAY_PIN
from irrigator import irrigate

# Assuming irrigator.py has the following structure
# from gpiozero import OutputDevice
# import time
#
# class MockOutputDevice:
#     def __init__(self, pin):
#         self.pin = pin
#         self.is_active = False
#         self.toggled_count = 0
#
#     def on(self):
#         self.is_active = True
#         self.toggled_count += 1
#
#     def off(self):
#         self.is_active = False
#         self.toggled_count += 1
#
# def irrigate(duration, relay_pin):
#     relay = MockOutputDevice(relay_pin) # Use MockOutputDevice here for direct testing
#     print(f"Turning on relay {relay_pin} for {duration} seconds")
#     relay.on()
#     time.sleep(duration)
#     relay.off()
#     print(f"Turning off relay {relay_pin}")

class TestIrrigator(unittest.TestCase):

    @patch('gpiozero.OutputDevice')
    def test_irrigate_function(self, MockOutputDevice):
        # Mock the instance of OutputDevice
        mock_relay_instance = MagicMock()
        mock_relay_instance.value = 0  # Configure the mock relay instance to have a 'value' attribute
        MockOutputDevice.return_value = mock_relay_instance

        duration = 5
        # We don't need relay_pin here as we are passing the mock instance

        with patch('time.sleep') as mock_sleep:
            # Call the function we are testing
            irrigate(duration, mock_relay_instance)

            # Assertions
            mock_relay_instance.on.assert_called_once()

            # Check if time.sleep was called with the correct duration
            mock_sleep.assert_called_once_with(duration)

            # Check if off() was called on the mocked relay instance
            mock_relay_instance.off.assert_called_once()

if __name__ == '__main__':
    unittest.main()
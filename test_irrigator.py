import unittest
from unittest.mock import patch, MagicMock

from irrigator import irrigate
from gpiozero.exc import GPIOZeroError # Import the real exception

class TestIrrigator(unittest.TestCase):

    def test_irrigate_success(self):
        # Create a mock relay object
        mock_relay = MagicMock()
        duration = 5
        # relay_pin is no longer needed in the irrigate function call
        # relay_pin = 17

    @patch('irrigator.Relay') # Patch the Relay class used in irrigator.py
    @patch('irrigator.gpiozero') # Patch the entire gpiozero library within irrigator.py
    def test_irrigate_gpiozeroerror_calls_off(self, MockGPIOZero):
        # Create a mock relay object
        mock_relay = MagicMock()
        # Configure the mock relay to raise GPIOZeroError on the 'on' call
        mock_relay.on.side_effect = GPIOZeroError("Simulated GPIO Error")

        duration = 5
        # relay_pin is no longer needed in the irrigate function call
        relay_pin = 17

        # Call the function, expecting it to handle the error
        irrigate(duration, relay_pin)

        # Assert that relay.off() was still called, even after the error
        # This test assumes the 'with' statement in irrigate handles the error
        # and ensures the 'off' and 'close' methods are called.
        mock_relay.on.assert_called_once() # The 'on' call raised the error
        mock_relay.off.assert_called_once()
        mock_relay.close.assert_called_once() # Ensure close is called due to 'with' statement

    def test_irrigate_success(self):
        # Create a mock relay object
        mock_relay = MagicMock()
        duration = 5
        # relay_pin is no longer needed in the irrigate function call
        # relay_pin = 17

        # Call the function to test, passing the mock relay
        irrigate(duration, mock_relay) # Pass the mock_relay

        # Assert that on and off methods were called on the mock relay instance
        mock_relay.on.assert_called_once()
        mock_relay.off.assert_called_once()
        # Ensure close is called due to 'with' statement even though the mock
        # doesn't strictly need __enter__ and __exit__ for this
        mock_relay.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
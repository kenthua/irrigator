import unittest
from unittest.mock import patch, MagicMock
import sys

# Mock schedule if not installed locally
if 'schedule' not in sys.modules:
    sys.modules['schedule'] = MagicMock()

from irrigator import irrigate, VenusRelay


class TestIrrigator(unittest.TestCase):

    def test_irrigate_normal_flow(self):
        mock_relay = MagicMock()
        mock_relay.value = 0

        duration = 5

        with patch("time.sleep") as mock_sleep:
            irrigate(duration, mock_relay)

            mock_relay.on.assert_called_once()
            mock_sleep.assert_called_once_with(duration)
            mock_relay.off.assert_called_once()

    def test_irrigate_exception_failsafe(self):
        """Verifies that relay.off() is guaranteed to run even if an exception occurs during time.sleep()."""
        mock_relay = MagicMock()
        mock_relay.value = 0

        duration = 5

        with patch("time.sleep", side_effect=RuntimeError("Simulated Sleep Interruption")):
            irrigate(duration, mock_relay)

            mock_relay.on.assert_called_once()
            # Crucial assertion: off() MUST be called via finally block despite exception
            mock_relay.off.assert_called_once()

    @patch("dbus.SystemBus")
    def test_venus_relay_dbus(self, mock_system_bus):
        mock_bus_instance = MagicMock()
        mock_obj = MagicMock()
        mock_iface = MagicMock()
        mock_iface.GetValue.return_value = 0

        mock_system_bus.return_value = mock_bus_instance
        mock_bus_instance.get_object.return_value = mock_obj

        mock_dbus = MagicMock()
        mock_dbus.SystemBus = mock_system_bus
        mock_dbus.Interface.return_value = mock_iface
        mock_dbus.Int32 = lambda x: x

        with patch.dict("sys.modules", {"dbus": mock_dbus}):
            relay = VenusRelay(relay_index=1)
            relay.use_dbus = True
            relay.iface = mock_iface

            relay.on()
            mock_iface.SetValue.assert_called_with(1)

            relay.off()
            mock_iface.SetValue.assert_called_with(0)

            self.assertEqual(relay.value, 0)


if __name__ == "__main__":
    unittest.main()
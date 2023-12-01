from unittest.mock import Mock
from CanBus import ModuleA
from CanBus import ModuleB
import can
import pytest
import time


@pytest.fixture
def can_bus():
    # Set up a mock version of the CAN interface for testing
    bus = Mock()
    bus.Message = can.Message  # Mock the Message class
    bus.recv.return_value = can.Message(arbitration_id=0x123,
                                        data=[0x01, 0x02, 0x03, 0x04])  # Set the desired received message
    yield bus
    # No need to clean up resources for a mock


def test_can_bus_integration(can_bus):
    # Test integration of CAN bus communication between different modules

    # Example data to be transmitted
    message_data = [0x01, 0x02, 0x03, 0x04]

    # Example modules communicating over CAN bus
    module_a = ModuleA(can_bus)
    module_b = ModuleB(can_bus)

    # Transmit a message from Module A
    module_a.transmit_message(message_data)

    # Wait until a message is received or a timeout occurs
    start_time = time.time()
    timeout = 1  # set your desired timeout in seconds
    received_message = None
    while time.time() - start_time < timeout:
        received_message = module_b.receive_message()
        if received_message:
            break

    # Check if a message is received within the timeout
    assert received_message is not None

    # Compare the entire received_message.data with message_data
    assert list(received_message.data) == message_data

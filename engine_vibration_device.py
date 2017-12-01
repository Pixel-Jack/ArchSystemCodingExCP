"""Virtual IOTile device for CoreTools Walkthrough
"""
import random
from iotile.core.hw.virtual.virtualdevice import VirtualIOTileDevice, rpc


class EngineVibrationVirtualDevice(VirtualIOTileDevice):
    """A simple virtual IOTile device that has three RPC :
        - 0x9000 that let you get and set min_value
        - 0x9001 that let you get and set max_value
        - 0x8000 that returns a random integer value between min_value and max_value
    Args:
        args (dict): {min_value: integer, max_value: integer}
    """

    def __init__(self, args):
        super(EngineVibrationVirtualDevice, self).__init__(1, 'Ngin01')
        self.min_value = 20
        self.max_value = 100
        # Create a worker that streams our realtime data every second
        self.create_worker(self._stream_temp, 1.0)

    def _stream_temp(self):
        """Send a fake vibration reading between min_value and max_value"""
        self.stream_realtime(0x1000, random.randint(self.min_value, self.max_value))

    @rpc(8, 0x0004, "", "H6sBBBB")
    def controller_status(self):
        """Return the name of the controller as a 6 byte string
        """
        status = (1 << 1) | (1 << 0)  # Report configured and running
        return [0xFFFF, self.name, 1, 0, 0, status]

    @rpc(8, 0x8000, "", "L")
    def get_vibration(self):
        """Send a fake vibration reading between min_value and max_value."""
        return [random.randint(self.min_value, self.max_value)]

    @rpc(8, 0x9000, "3sL", "L")
    def manage_min_value(self, order, val):
        """
        Allow the user to see or change the value of min_value
        Warning : if set=value with value >= max_value there will be no changes
        :param order: get or set
        :param val: integer (type unsigned long 0 <= number <= 4294967295)
        :return: min_value integer
        """
        if order == 'set':
            if val < self.max_value:
                self.min_value = val
        return [self.min_value]

    @rpc(8, 0x9001, "3sL", "L")
    def manage_max_value(self, order, val):
        """
        Allow the user to see or change the value of max_value
        Warning : if set=value with value <= min_value there will be no changes
        :param order: get or set
        :param val: integer (type unsigned long 0 <= number <= 4294967295)
        :return: max_value integer
        """
        if order == 'set':
            if val > self.min_value:
                self.max_value = val
        return [self.max_value]

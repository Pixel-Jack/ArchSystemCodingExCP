from iotile.core.hw.proxy.proxy import TileBusProxyObject
from iotile.core.utilities.typedargs.annotate import return_type, context, param
import struct


@context("EngineVibrationProxy")
class EngineVibrationProxyObject(TileBusProxyObject):
    """A engine_vibration proxy object for the CoreTools walkthrough
    """

    @classmethod
    def ModuleName(cls):
        """The 6 byte name by which CoreTools matches us with an IOTile Device
        """
        return 'Ngin01'

    @return_type("integer")
    def get_vibration(self):
        temp, = self.rpc(0x80, 0x00, result_format="L")
        return temp

    @return_type("integer")
    @param("manage_value", "string")
    def manage_min_value(self, manage_value):
        """
        Function to manage the min_value we can get it with get or set it with set=integer
        ex : manage_min_value get => return min_value
            manage_min_value set=3456 => set min_value and return min_value
        Warning : if set=value with value >= max_value there will be no changes
        :param manage_value: get or set=integer
        :return: min_value integer
        """
        data = manage_value.split("=")
        if data[0].lower() in ['set', 'get'] and len(data) < 3:
            # get ride of entry like set=345= or other things like that
            if len(data) == 2:
                # that's mean that there is a value after the =
                try:
                    new_value = int(data[1])
                except ValueError:
                    print("Incorrect value entry {}".format(data[1]))
                    return
            else:
                new_value = 0
            # Now everything is clean and ready to be sent to the device
            args = struct.pack("<3sL", data[0].lower(), new_value)
            vibration_min_value, = self.rpc(0x90, 0x00, args, result_format="L")
            return vibration_min_value
        else:
            print("Incorrect entry {}".format(manage_value))
            return

    @return_type("integer")
    @param("manage_value", "string")
    def manage_max_value(self, manage_value):
        """
        Function to manage the max_value we can get it with get or set it with set=integer
        ex : manage_max_value get => return max_value
            manage_max_value set=3456 => set max_value and return max_value
        Warning : if set=value with value <= min_value there will be no changes
        :param manage_value: get or set=integer
        :return: max_value integer
        """
        data = manage_value.split("=")
        if data[0].lower() in ['set', 'get'] and len(data) < 3:
            # get ride of entry like set=345= or other things like that
            if len(data) == 2:
                # that's mean that there is a value after the =
                try:
                    new_value = int(data[1])
                except ValueError:
                    print("Incorrect value entry {}".format(data[1]))
                    return
            else:
                new_value = 0
            # Now everything is clean and ready to be sent to the device
            args = struct.pack("<3sL", data[0].lower(), new_value)
            vibration_max_value, = self.rpc(0x90, 0x01, args, result_format="L")
            return vibration_max_value
        else:
            print("Incorrect entry {}".format(manage_value))
            return

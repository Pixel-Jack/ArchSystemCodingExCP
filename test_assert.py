import pytest
import subprocess

from iotile.core.hw.hwmanager import HardwareManager, APIError

subprocess.call(["iotile","registry","add_component","test_component/."])

def vibration_test(min, max, con):
    for i in range(100):
        vibration = con.get_vibration()
        assert isinstance(vibration, int)
        assert min <= vibration <= max

def test_initialisation():
    with HardwareManager(port='virtual:./engine_vibration_device.py') as hw:
        hw.connect('1')
        con = hw.controller()
        assert con.manage_min_value('get') == 20
        assert con.manage_max_value('get') == 100
        vibration_test(20, 100, con)



def test_set_correct_max_value():
    with HardwareManager(port='virtual:./engine_vibration_device.py') as hw:
        hw.connect('1')
        con = hw.controller()
        assert con.manage_max_value('set=21') == 21
        vibration_test(20, 21, con)
        assert con.manage_max_value('set=1234567890') == 1234567890
        vibration_test(20, 1234567890, con)


def test_set_incorrect_max_value():
    with HardwareManager(port='virtual:./engine_vibration_device.py') as hw:
        hw.connect('1')
        con = hw.controller()
        assert con.manage_max_value('set=20') == 100 # initial value
        assert con.manage_max_value('set=0') == 100
        assert con.manage_max_value('set=zhrbjvk') == None
        with pytest.raises(APIError):
            con.manage_max_value('set=-1')
        with pytest.raises(APIError):
            con.manage_max_value('set=1000000000000000000000000')
        with pytest.raises(APIError):
            # message="APIError: (\"'L' format requires 0 <= number <= 4294967295\",)"
            con.manage_max_value('set=12345678900')


def test_set_correct_min_value():
    with HardwareManager(port='virtual:./engine_vibration_device.py') as hw:
        hw.connect('1')
        con = hw.controller()
        assert con.manage_min_value('set=99') == 99
        vibration_test(99, 100, con)
        assert con.manage_min_value('set=0') == 0
        vibration_test(0, 100, con)

def test_set_incorrect_min_value():
    with HardwareManager(port='virtual:./engine_vibration_device.py') as hw:
        hw.connect('1')
        con = hw.controller()
        assert con.manage_min_value('set=100') == 20 # initial value
        assert con.manage_min_value('set=zhrbjvk') == None
        with pytest.raises(APIError):
            con.manage_min_value('set=-1')
        with pytest.raises(APIError):
            # since min_value is converted in long before being compared to max_value this kind of error can appear
            con.manage_min_value('set=10000000000000000000000000000000000000')

def test_crossed_changes():
    with HardwareManager(port='virtual:./engine_vibration_device.py') as hw:
        hw.connect('1')
        con = hw.controller()
        assert con.manage_min_value('set=55') == 55
        vibration_test(55, 100, con)
        assert con.manage_max_value('set=20') == 100 # initial value
        vibration_test(55, 100, con)
        assert con.manage_min_value('set=550') == 55
        vibration_test(55, 100, con)
        assert con.manage_max_value('set=20000') == 20000 # initial value
        vibration_test(55, 20000, con)
        assert con.manage_max_value('set=zhrbjvk') == None
        vibration_test(55, 20000, con)



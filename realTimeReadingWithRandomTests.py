from iotile.core.hw.hwmanager import HardwareManager
from iotile.core.hw.reports import IndividualReadingReport, IOTileReading
import random

with HardwareManager(port='virtual:./engine_vibration_device.py') as hw:
    hw.connect('1')
    hw.enable_streaming()
    con = hw.controller()

    # hw.iter_reports() will run forever until we kill the program
    # with a control-c so make sure to catch that and cleanly exit
    # without printing an exception stacktrace.
    random_change_max = 0
    random_change_min = 0
    try:
        for report in hw.iter_reports(blocking=True):
            # Verify that the device is sending realtime data as we expect
            assert isinstance(report, IndividualReadingReport)
            assert len(report.visible_readings) == 1

            reading = report.visible_readings[0]
            min_value = con.manage_min_value('get')
            max_value = con.manage_max_value('get')
            assert min_value < reading.value < max_value
            print("min_value: {0} < Reading: {1} < max_value: {2}".format(min_value, reading.value, max_value))
            assert isinstance(reading, IOTileReading)
            print("Received {}".format(reading))

            ### VARIATIONS
            ### If the prompt show a new value which is the same as the last one its because we tried to set a value incorrect
            ## for instance if we tried to put a min_value > max_value there will be no change
            if random_change_max == 0:
                new_max = random.randint(-100, 100000)
                try:
                    print("New max : {}".format(con.manage_max_value('set={}'.format(new_max))))
                except:
                    print("No change of max value")
                random_change_max = random.randint(1, 15)
            if random_change_min == 0:
                new_min = random.randint(-100, 100000)
                try:
                    print("New min : {}".format(con.manage_min_value('set={}'.format(new_min))))

                except:
                    print("No change of min value")
                random_change_min = random.randint(1, 15)

            random_change_max -= 1
            random_change_min -= 1


    except KeyboardInterrupt:
        pass

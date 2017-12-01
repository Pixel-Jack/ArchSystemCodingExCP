from iotile.core.hw.hwmanager import HardwareManager
from iotile.core.hw.reports import IndividualReadingReport, IOTileReading

with HardwareManager(port='virtual:./engine_vibration_device.py') as hw:
    hw.connect('1')
    hw.enable_streaming()
    # hw.iter_reports() will run forever until we kill the program
    # with a control-c so make sure to catch that and cleanly exit
    # without printing an exception stacktrace.
    try:
        for report in hw.iter_reports(blocking=True):
            assert isinstance(report, IndividualReadingReport)
            assert len(report.visible_readings) == 1
            reading = report.visible_readings[0]
            assert isinstance(reading, IOTileReading)

            print("Received {}".format(reading))
    except KeyboardInterrupt:
        pass
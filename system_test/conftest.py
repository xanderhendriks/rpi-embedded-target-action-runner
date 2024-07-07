import pytest
import platform
import serial
import time

from threading import Thread


if platform.uname().machine.startswith('arm'):
    import RPi.GPIO as GPIO


class SerialCommandResponse:
    def __init__(self, port):
        self.thread = None
        self.serial = serial.Serial(port, 9600, timeout=1)
        self.serial.read(1000)

    def command(self, command):
        self.response_string = None
        self.thread = Thread(target=self._process)
        self.thread.start()
        self.serial.write(command.encode())

    def response(self, timeout=0.5):
        start_time = time.time()
        while self.response_string is None and time.time() < (start_time + timeout):
            pass
        time.sleep(1)
        self.thread.join()
        return self.response_string

    def _process(self):
        """
        Process for reading the serial debug port
        """
        self.response_string = self.serial.readline().decode().rstrip()


@pytest.fixture(scope="session")
def serial_command_response(pytestconfig):
    return SerialCommandResponse(pytestconfig.config.getoption('--st-link-com-port'))


class PowerControl():
    GPIO_POWER_CONTROL = 18

    def rpi_check_decorator(function):
        def wrapper(self, *args, **kwargs):
            if platform.uname().machine.startswith('arm'):
                function(self, *args, **kwargs)
            else:
                print('Power control only working on RPi')
        return wrapper

    @rpi_check_decorator
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.GPIO_POWER_CONTROL, GPIO.OUT)

    @rpi_check_decorator
    def power_off(self):
        GPIO.output(self.GPIO_POWER_CONTROL, GPIO.HIGH)

    @rpi_check_decorator
    def power_on(self):
        GPIO.output(self.GPIO_POWER_CONTROL, GPIO.LOW)

    @rpi_check_decorator
    def power_cycle(self, delay_ms=0):
        self.power_off()
        time.sleep(delay_ms / 1000)
        self.power_on()


@pytest.fixture
def power_control():
    return PowerControl()


def pytest_addoption(parser):
    parser.addoption("--version-to-check", action="store", default="0.0.0")
    parser.addoption("--git-hash-to-check", action="store", default="debugbuild")
    parser.addoption('--st-link-com-port', action='store', default='/dev/ttyACM0')


def pytest_generate_tests(metafunc):
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".
    option_value = metafunc.config.option.version_to_check
    if 'version_to_check' in metafunc.fixturenames:
        metafunc.parametrize('version_to_check', [option_value])

    option_value = metafunc.config.option.git_hash_to_check
    if 'git_hash_to_check' in metafunc.fixturenames:
        metafunc.parametrize('git_hash_to_check', [option_value])

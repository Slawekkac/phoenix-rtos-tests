#
# Phoenix-RTOS test runner
#
# IMXRT117x runner
#
# Copyright 2021 Phoenix Systems
# Authors: Damian Loewnau, Jakub Sarzyński
#

import time
import sys
from pexpect.exceptions import TIMEOUT, EOF

from .common import DeviceRunner, PloTalker, PloError, Psu, Phoenixd, PhoenixdError, GPIO, Color, logging
from .common import phd_error_msg, rootfs

class IMXRT117xRunner(DeviceRunner):
    """This class provides interface to run test case on IMXRT117x using RaspberryPi.
       GPIO 4 must be connected to the pin 4 in P1 Header (using a resistor 5,1k).
       GPIO 2 must be connected to an appropriate IN pin in relay module"""

    SDP = 'plo-ram-armv7m7-imxrt117x.sdp'
    IMAGE = 'phoenix-armv7m7-imxrt117x.disk'

    def __init__(
        self,
        port,
        phoenixd_port='/dev/serial/by-id/usb-Phoenix_Systems_plo_CDC_ACM-if00'
    ):
        super().__init__(port)
        self.phoenixd_port = phoenixd_port
        self.power_gpio = GPIO(2)
        self.power_gpio.high()
        self.boot_gpio = GPIO(4)
        self.ledr_gpio = GPIO(13)
        self.ledg_gpio = GPIO(18)
        self.ledb_gpio = GPIO(12)
        self.ledb_gpio.high()

    def led(self, color, state="on"):
        if state == "on" or state == "off":
            self.ledr_gpio.low()
            self.ledg_gpio.low()
            self.ledb_gpio.low()
        if state == "on":
            if color == "red":
                self.ledr_gpio.high()
            if color == "green":
                self.ledg_gpio.high()
            if color == "blue":
                self.ledb_gpio.high()

    def _restart_by_poweroff(self):

        self.power_gpio.low()
        time.sleep(0.500)
        self.power_gpio.high()
        time.sleep(0.500)

    def reboot(self, serial_downloader=False):
        if serial_downloader:
            self.boot_gpio.high()
        else:
            self.boot_gpio.low()

        self._restart_by_poweroff()

    def flash(self):
        self.reboot(serial_downloader=True)

        phd = None
        try:
            with PloTalker(self.port) as plo:
                Psu(script=self.SDP).run()
                plo.wait_prompt()
                with Phoenixd(self.phoenixd_port) as phd:
                    plo.copy_file2mem(
                        src='usb0',
                        file=self.IMAGE,
                        dst='flash0',
                        off=0
                    )
        except (TIMEOUT, EOF, PloError, PhoenixdError) as exc:
            exception = f'{exc}\n'
            if phd:
                exception = phd_error_msg(exception, phd.output())

            logging.info(exception)
            sys.exit(1)

        self.reboot()

    def load(self, test):
        """Loads test ELF into syspage using plo"""
        phd = None
        load_dir = str(rootfs(test.target) / 'bin')
        self.reboot()
        try:
            with PloTalker(self.port) as plo:
                plo.wait_prompt()

                if not test.exec_cmd:
                    # We got plo prompt, we are ready for sending the "go!" command.
                    return True

                with Phoenixd(self.phoenixd_port, dir=load_dir) as phd:
                    plo.app('usb0', test.exec_cmd[0], 'ocram2', 'ocram2')
        except (TIMEOUT, EOF, PloError, PhoenixdError) as exc:
            if isinstance(exc, PloError) or isinstance(exc, PhoenixdError):
                test.exception = str(exc)
                test.fail()
            else:  # TIMEOUT or EOF
                test.exception = Color.colorify('EXCEPTION PLO\n', Color.BOLD)
                test.handle_pyexpect_error(plo.plo, exc)

            if phd:
                test.exception = phd_error_msg(test.exception, phd.output())

            return False

        return True

    def run(self, test):
        if test.skipped():
            return

        if not self.load(test):
            return

        super().run(test)

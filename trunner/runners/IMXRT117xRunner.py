#
# Phoenix-RTOS test runner
#
# IMXRT117x runner
#
# Copyright 2021 Phoenix Systems
# Authors: Damian Loewnau, Jakub Sarzyński
#

import time

from .common import ARMV7M7Runner, GPIO


class IMXRT117xRunner(ARMV7M7Runner):
    """This class provides interface to run test case on IMXRT117x using RaspberryPi.
       GPIO 4 must be connected to the pin 4 in P1 Header (using a resistor 3,3k).
       GPIO 2 must be connected to an appropriate IN pin in relay module
       GPIO 13 must be connected to a red LED
       GPIO 18 must be connected to a green LED
       GPIO 12 must be connected to a blue LED"""

    SDP = 'plo-ram-armv7m7-imxrt117x.sdp'
    IMAGE = 'phoenix-armv7m7-imxrt117x.disk'

    def __init__(
        self,
        port,
        phoenixd_port='/dev/serial/by-id/usb-Phoenix_Systems_plo_CDC_ACM-if00',
    ):
        super().__init__(port)
        self.phoenixd_port = phoenixd_port
        self.is_cut_power_used = True
        self.flash_memory = 0
        self.power_gpio = GPIO(2)
        self.power_gpio.high()
        self.boot_gpio = GPIO(4)
        self.ledr_gpio = GPIO(13)
        self.ledg_gpio = GPIO(18)
        self.ledb_gpio = GPIO(12)
        self.ledb_gpio.high()

    def led(self, color, state="on"):
        super().led(color=color, state=state)

    def _restart_by_poweroff(self):

        self.power_gpio.low()
        time.sleep(0.500)
        self.power_gpio.high()
        time.sleep(0.500)

    def reboot(self, serial_downloader=False, cut_power=True):
        if serial_downloader:
            self.boot_gpio.high()
        else:
            self.boot_gpio.low()

        self._restart_by_poweroff()

    def run(self, test):
        super().run(test)

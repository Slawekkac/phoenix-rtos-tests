#
# Phoenix-RTOS test runner
#
# IMXRT1064 runner
#
# Copyright 2021 Phoenix SYstems
# Authors: Jakub Sarzyński, Mateusz Niewiadomski, Damian Loewnau
#

import time
import sys

from .common import ARMV7M7Runner, GPIO, logging
from .common import unbind_rpi_usb, power_usb_ports, wait_for_dev


class IMXRT106xRunner(ARMV7M7Runner):
    """This class provides interface to run test case on IMXRT106x using RaspberryPi.
       GPIO 17 must be connected to the JTAG_nSRST (j21-15) (using an additional resistor 1,5k).
       GPIO 4 must be connected to the SW7-3 (using a resistor 4,3k).
       GPIO 2 must be connected to an appropriate IN pin in relay module"""

    SDP = 'plo-ram-armv7m7-imxrt106x.sdp'
    IMAGE = 'phoenix-armv7m7-imxrt106x.disk'

    def __init__(
        self,
        port,
        phoenixd_port='/dev/serial/by-id/usb-Phoenix_Systems_plo_CDC_ACM-if00',
        is_cut_power_used=False,
    ):
        super().__init__(port[0])
        self.port_usb = port[1]
        self.phoenixd_port = phoenixd_port
        self.is_cut_power_used = is_cut_power_used
        self.flash_memory = 1
        self.reset_gpio = GPIO(17)
        self.reset_gpio.high()
        self.power_gpio = GPIO(2)
        self.power_gpio.high()
        self.boot_gpio = GPIO(4)

    def led(self, color, state="on"):
        super().led(color=color, state=state)

    def _restart_by_jtag(self):
        self.reset_gpio.low()
        time.sleep(0.050)
        self.reset_gpio.high()

    def _restart_by_poweroff(self):
        unbind_rpi_usb(self.port_usb)

        power_usb_ports(False)
        self.power_gpio.low()
        time.sleep(0.500)
        self.power_gpio.high()
        time.sleep(0.500)
        power_usb_ports(True)

        try:
            wait_for_dev(self.port_usb, timeout=30)
        except TimeoutError:
            logging.error('Serial port not found!\n')
            sys.exit(1)

    def reboot(self, serial_downloader=False, cut_power=False):
        if serial_downloader:
            self.boot_gpio.low()
        else:
            self.boot_gpio.high()

        if cut_power:
            self._restart_by_poweroff()
        else:
            self._restart_by_jtag()

    def run(self, test):
        super().run(test)

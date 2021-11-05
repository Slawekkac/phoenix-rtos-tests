#
# Phoenix-RTOS test runner
#
# Stm32l4 runner
#
# Copyright 2021 Phoenix SYstems
# Authors: Mateusz Niewiadomski
#

import os
import subprocess
import sys
import time

import pexpect.fdpexpect
import serial

from .common import DeviceRunner, Color
from .common import _BOOT_DIR


class STM32L4Runner(DeviceRunner):
    """ This class provides interface to run test case on STM32L4 target using RaspberryPi.
        The ST-Link programming board should be connected to USB port
        and a target should be connected to ST-Link and powered"""

    class oneByOne_fdspawn(pexpect.fdpexpect.fdspawn):
        """ Workaround for Phoenix-RTOS on stm32l4 targets not processing characters fast enough
            This class inherits and is passed to harness instead of pexpect.fdpexpect.fdspawn
            It redefines send() with addition of timeout after each letter sent. Timeout set to 50ms per character"""

        def send(self, string):
            ret = 0
            for char in string:
                ret += super().send(char)
                time.sleep(0.03)
            return ret

    def flash(self):
        """ Flashing with openocd as a separate process """

        binary_path = os.path.join(_BOOT_DIR, 'phoenix-armv7m4-stm32l4x6.bin')
        openocd_cmd = [
            'openocd',
            '-f', 'interface/stlink.cfg',
            '-f', 'target/stm32l4x.cfg',
            '-c', "reset_config srst_only srst_nogate connect_assert_srst",
            '-c',  "program {progname} 0x08000000 verify reset exit".format(progname=binary_path)
            ]
        openocd_process = subprocess.Popen(
            openocd_cmd,
            stdout=subprocess.PIPE,
            stderr=sys.stdout.fileno()
            )
        try:
            assert openocd_process.wait() == 0
        except AssertionError:
            print(Color.colorify("OpenOCD error: cannot flash target\n", Color.BOLD))
            exit(1)

    def run(self, test):
        if test.skipped():
            return

        try:
            self.serial = serial.Serial(self.port, baudrate=115200)
        except serial.SerialException:
            test.handle_exception()
            return

        # Create pexpect.fdpexpect.fdspawn with modified send() by using oneByOne_fdspawn class
        # codec_errors='ignore' - random light may cause out-of-ascii characters to appear when using optical port
        proc = self.oneByOne_fdspawn(
            self.serial,
            encoding='ascii',
            codec_errors='ignore',
            timeout=test.timeout
            )

        # FIXME - race on start of Phoenix-RTOS between dummyfs and psh
        # sending newline ensures that carret is in newline just after (psh)% prompt
        proc.send("\n")

        try:
            test.handle(proc)
        finally:
            self.serial.close()

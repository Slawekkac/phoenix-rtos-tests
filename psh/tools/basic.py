
# Phoenix-RTOS
#
# phoenix-rtos-tests
#
# basic tools for psh related tests
#
# Copyright 2021 Phoenix Systems
# Author: Jakub Sarzyński, Damian Loewnau
#
# This file is part of Phoenix-RTOS.
#
# %LICENSE%
#

import pexpect
import re

PROMPT = r'\r\x1b\[0J' + r'\(psh\)% '
EOL = r'(\r+)\n'


class Psh:
    """The interface to communicate with psh in tests"""
    def __init__(self, pexpect_proc):
        self.p = pexpect_proc

    def assert_expected(self, input, expected, msg=''):
        self.p.sendline(input)
        expected = input + EOL + expected + EOL + PROMPT
        msg = f'Expected output regex was: \n---\n{expected}\n---\n' + msg
        assert self.p.expect([expected, pexpect.TIMEOUT]) == 0, msg

    def run(self):
        self.p.send('psh\r\n')
        self.p.expect(r'psh(\r+)\n')

    def assert_only_prompt(self):
        # Expect an erase in display ascii escape sequence and a prompt sign
        prompt = '\r\x1b[0J' + '(psh)% '
        got = self.p.read(len(prompt))
        assert got == prompt, f'Expected:\n{prompt}\nGot:\n{got}'

    def assert_prompt(self, msg=None, timeout=-1, catch_timeout=True):
        if not msg:
            msg = ''

        patterns = ['(psh)% ']
        if catch_timeout:
            patterns.append(pexpect.TIMEOUT)

        idx = self.p.expect_exact(patterns, timeout=timeout)
        # if catch_timeout is false then pyexpect exception is raised
        assert idx == 0, msg

    def assert_prompt_fail(self, msg=None, timeout=-1):
        if not msg:
            msg = ''

        patterns = ['(psh)% ', pexpect.TIMEOUT]
        idx = self.p.expect_exact(patterns, timeout=timeout)
        assert idx == 1, msg

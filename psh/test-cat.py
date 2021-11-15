# Phoenix-RTOS
#
# phoenix-rtos-tests
#
# psh cat command test
#
# Copyright 2021 Phoenix Systems
# Author: Damian Loewnau
#
# This file is part of Phoenix-RTOS.
#
# %LICENSE%
#

from psh.tools.basic import Psh

PROMPT = r'\r\x1b\[0J' + r'\(psh\)% '


def is_hardware_target(p):
    cmd = 'ls'

    p.sendline(cmd)
    p.expect(cmd)
    idx = p.expect([
            'syspage',
            'bin'])
    p.expect(PROMPT)

    if idx == 0:
        return True
    elif idx == 1:
        return False


def assert_cat_err():
    fname = 'nonexistentFile'
    cmd = f'cat {fname}'
    statement = f'cat: {fname} no such file'

    psh.assert_expected(input=cmd, expected=statement)


def assert_cat_h():
    cmd = 'cat -h'
    help = r'Usage: cat \[options\] \[files\](\r+)\n' \
        + r'  -h:  shows this help message'

    psh.assert_expected(input=cmd, expected=help)


def assert_cat_shells():
    fname = 'etc/shells'
    fcontent = '# /etc/shells: valid login shells(\r+)\n/bin/sh'
    cmd = f'cat {fname}'

    psh.assert_expected(input=cmd, expected=fcontent)


def harness(p):
    global psh
    psh = Psh(p)
    psh.run()
    psh.assert_only_prompt()

    # need to add more test cases when it will be possible to write content to the file
    assert_cat_err()
    assert_cat_h()

    # there are no files on imxrt106x target that can be written out
    if not is_hardware_target(p):
        assert_cat_shells()

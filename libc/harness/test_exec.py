# Phoenix-RTOS
#
# libc-tests
#
# various exec functions tests
#
# Copyright 2021 Phoenix Systems
# Author: Damian Loewnau
#
# This file is part of Phoenix-RTOS.
#
# %LICENSE%
#

from psh.tools.basic import Psh


def assert_execve_env_changed():
    cmd = '/bin/test_exec 1'
    result = (r'(argc = 1(\r+)\n)'
                r'(argv\[0\] = /bin/to_exec(\r+)\n)'
                r'(environ\[0\] = TEST1=exec_value)')

    psh.assert_expected(input=cmd, expected=result, msg="Wrong output of execve function with changed environment")


def assert_execve_env_unchanged():
    cmd = '/bin/test_exec 2'
    result = (r'(argc = 1(\r+)\n)'
                r'(argv\[0\] = /bin/to_exec(\r+)\n)'
                r'(environ\[0\] = TEST1=unchanged_value)')

    psh.assert_expected(input=cmd, expected=result, msg="Wrong output of execve function with unchanged environment")


def assert_execve_path_searched():
    cmd = '/bin/test_exec 3'
    result = (r'(argc = 1(\r+)\n)'
                r'(argv\[0\] = to_exec(\r+)\n)'
                r'(environ\[0\] = PATH=/bin:/sbin:/usr/bin:/usr/sbin)')

    psh.assert_expected(input=cmd, expected=result, msg="Wrong output of execve function with searching in PATH environment variable")


def assert_execvpe_env_changed():
    cmd = '/bin/test_exec 4'
    result = (r'(argc = 1(\r+)\n)'
                r'(argv\[0\] = /bin/to_exec(\r+)\n)'
                r'(environ\[0\] = TEST1=exec_value)')

    psh.assert_expected(input=cmd, expected=result, msg="Wrong output of execvpe function with changed environment")


def assert_execvpe_env_unchanged():
    cmd = '/bin/test_exec 5'
    result = (r'(argc = 1(\r+)\n)'
                r'(argv\[0\] = /bin/to_exec(\r+)\n)'
                r'(environ\[0\] = TEST1=unchanged_value)')

    psh.assert_expected(input=cmd, expected=result, msg="Wrong output of execvpe function with unchanged environment")


def assert_execvpe_path_searched():
    cmd = '/bin/test_exec 6'
    result = (r'(argc = 1(\r+)\n)'
                r'(argv\[0\] = to_exec(\r+)\n)'
                r'(environ\[0\] = PATH=/bin:/sbin:/usr/bin:/usr/sbin)')

    psh.assert_expected(input=cmd, expected=result, msg="Wrong output of execvpe function with searching in PATH environment variable")


def assert_execvp_env_unchanged():
    cmd = '/bin/test_exec 7'
    result = (r'(argc = 1(\r+)\n)'
                r'(argv\[0\] = /bin/to_exec(\r+)\n)'
                r'(environ\[0\] = TEST1=unchanged_value)')

    psh.assert_expected(input=cmd, expected=result, msg="Wrong output of execvp function with unchanged environment")


def assert_execvp_path_searched():
    cmd = '/bin/test_exec 8'
    result = (r'(argc = 1(\r+)\n)'
                r'(argv\[0\] = to_exec(\r+)\n)'
                r'(environ\[0\] = PATH=/bin:/sbin:/usr/bin:/usr/sbin)')

    psh.assert_expected(input=cmd, expected=result, msg="Wrong output of execvp function with searching in PATH environment variable")


def harness(p):
    global psh
    psh = Psh(p)
    psh.run()
    psh.assert_only_prompt()

    assert_execve_env_changed()
    assert_execve_env_unchanged()
    assert_execve_path_searched()
    assert_execvpe_env_changed()
    assert_execvpe_env_unchanged()
    assert_execvpe_path_searched()
    assert_execvp_env_unchanged()
    assert_execvp_path_searched()

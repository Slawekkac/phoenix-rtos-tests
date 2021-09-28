# Phoenix-RTOS
#
# phoenix-rtos-tests
#
# psh kill command test
#
# Copyright 2021 Phoenix Systems
# Author: Damian Loewnau
#
# This file is part of Phoenix-RTOS.
#
# %LICENSE%
#

from psh.tools.basic import run_psh, assert_only_prompt
from time import sleep

PROMPT = r'\r\x1b\[0J' + r'\(psh\)% '
EOL = r'(\r+)\n'


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


def get_process_list(p):
    header_seen = False
    ps_header = 'PID PPID PR STATE %CPU WAIT TIME VMEM THR CMD'.split()
    ps_list = []
    oneline_pattern = r'(.*?)(\r+)\n'
    cmd = 'ps'
    p.sendline(cmd)
    p.expect(cmd + EOL)
    while True:
        idx = p.expect([PROMPT, oneline_pattern])
        if idx == 0:
            break
        line = p.match.group(1)
        if not header_seen and line.split() == ps_header:
            header_seen = True
        else:
            try:
                pid, ppid, pr, state, cpu, wait, time, vmem, thr, task = line.split()
            except ValueError:
                assert False, f'wrong ps output: {line}'

            ps_list.append({'pid': pid, 'task': task, 'state': state})

    return ps_list


def create_psh_processes(p, count):
    psh_pid_list = []
    if not is_hardware_target(p):
        cmd = '/bin/psh'
    else:
        cmd = 'sysexec psh'

    for i in range(count):
        p.sendline(cmd)
        p.expect(cmd + EOL)
    p.expect(PROMPT)
    ps_list = get_process_list(p)
    # find pid list of sleep psh processes
    for proc in ps_list:
        task = proc.get('task')
        if proc.get('state') == 'sleep' and (task == 'psh' or task == cmd):
            psh_pid_list.append(proc.get('pid'))

    psh_pid_count = len(psh_pid_list)
    assert psh_pid_count == count, f'Created {psh_pid_count} psh processes, instead of {count}'

    return psh_pid_list


def assert_kill_procs(p, pid_list, pid_count):
    for i in range(pid_count):
        cmd = f'kill {pid_list[i]}'
        p.sendline(cmd)
        p.expect(cmd + EOL)
    sleep(0.5)
    ps_list = get_process_list(p)

    for nr in range(pid_count):
        assert {'pid': pid_list[nr], 'task': f'test_proc_{nr}'} not in ps_list, \
            f'The process with id: {pid_list[nr]} is still in the processes list, even though it has been killed'


def assert_kill_nonexistent_proc(p):
    pid = 90
    used_pid_list = []
    ps_list = get_process_list(p)

    for proc in ps_list:
        used_pid_list.append(proc.get('pid'))

    # if process id is used, find next unused id
    while f'{pid}' in used_pid_list:
        pid = pid + 1

    cmd = f'kill {pid}'
    p.sendline(cmd)
    # nothing should be done
    p.expect(cmd + EOL + PROMPT)


def assert_kill_noarg(p):
    cmd = 'kill'
    info = 'usage: kill <pid>'

    p.sendline(cmd)
    p.expect(cmd + EOL + info + EOL + PROMPT)


def assert_kill_strarg(p):
    strarg = 'not_number'
    cmd = f'kill {strarg}'
    statement = f'kill: could not parse process id: {strarg}'

    p.sendline(cmd)
    p.expect(cmd + EOL + statement + EOL + PROMPT)


def harness(p):

    run_psh(p)
    assert_only_prompt(p)

    assert_kill_noarg(p)
    assert_kill_strarg(p)
    assert_kill_nonexistent_proc(p)
    pid_list = create_psh_processes(p, 3)
    assert_kill_procs(p, pid_list, 3)

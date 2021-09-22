# Phoenix-RTOS
#
# phoenix-rtos-tests
#
# psh ls command test
#
# Copyright 2021 Phoenix Systems
# Author: Damian Loewnau
#
# This file is part of Phoenix-RTOS.
#
# %LICENSE%
#

from psh.tools.basic import run_psh, assert_only_prompt

PSH_COMMANDS = [
    'bind',
    'cat',
    'edit',
    'exec',
    'help',
    'kill',
    'ls',
    'mem',
    'mkdir',
    'mount',
    'nc',
    'nslookup',
    'perf',
    'ping',
    'ps',
    'pshapp',
    'reboot',
    'runfile',
    'sync',
    'sysexec',
    'top',
    'touch',
    'uptime']

PROMPT = r'\r\x1b\[0J' + r'\(psh\)% '
EOL = r'((\r+)\n)'

esc_codes = {
    'set_blue': r'\x1b\[34m',
    'set_green': r'\033\[32m',
    'set_yellowonblack': r'\033\[33;40m',
    'reset_attributes': r'\x1b\[0m'
}


def assert_allfiles_occurence(p, files):
    # there can be other files in list
    other_file_pattern = r'(' + r'(\S+)[ \t]*' + esc_codes["reset_attributes"] + EOL + r'?)*?'
    exp_list = r'(' + esc_codes['set_green'] + r'('
    for pshcmd in files:
        if pshcmd != files[0]:
            exp_list = exp_list + r'|'
        exp_list = exp_list + pshcmd

    exp_list = exp_list + r')[ \t]*' + esc_codes["reset_attributes"] + EOL + '?'
    exp_list = exp_list + other_file_pattern + r'){' + f'{len(files)}' + r'}'

    p.expect(exp_list)


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


def create_intdir(p):
    cmd = 'mkdir testDir/dir'
    p.sendline(cmd)
    p.expect(cmd + EOL)


def create_testfiles(p, files):
    cmd = 'touch '
    for file in files:
        if file == 'dir':
            continue
        cmd += f'testDir/{file} '
        p.sendline(cmd)
        p.expect(cmd + EOL)


def create_testdir(p):
    cmd = 'mkdir testDir'
    p.sendline(cmd)
    p.expect(cmd + EOL)


def assert_ls_err(p):
    fileName = 'nonexistentFile'
    cmd = f'ls {fileName}'
    statement = f"ls: can't access {fileName}: no such file or directory"
    p.sendline(cmd)
    p.expect(cmd + EOL + statement + EOL + PROMPT)

    return True


def assert_ls_noarg(p, files):
    cmd = 'ls testDir'
    exp_list = ''
    for file in sorted(files):
        if file == 'dir':
            exp_list += esc_codes['set_blue']
        if file[0] == '.':
            continue
        # last position
        if file == sorted(files)[len(files)-1]:
            exp_list += f'{file}' + esc_codes['reset_attributes']
        else:
            exp_list += f'{file}  ' + esc_codes['reset_attributes']

    p.sendline(cmd)
    p.expect(cmd + EOL + exp_list + EOL + PROMPT)


def assert_ls_1(p, files):
    cmd = 'ls -1 testDir'
    exp_list = ''
    for file in sorted(files):
        if file == 'dir':
            exp_list += esc_codes['set_blue']
        if file[0] == '.':
            continue
        # last position
        if file == sorted(files)[len(files)-1]:
            exp_list += f'{file}' + esc_codes['reset_attributes']
        else:
            exp_list += f'{file}' + esc_codes['reset_attributes'] + EOL

    p.sendline(cmd)
    p.expect(cmd + EOL + exp_list + EOL + PROMPT)


def assert_ls_a(p, files):
    cmd = 'ls -a testDir'
    exp_list = esc_codes['set_blue'] \
        + '.  ' \
        + esc_codes['reset_attributes'] \
        + esc_codes['set_blue'] \
        + '..  ' \
        + esc_codes['reset_attributes']

    for file in sorted(files):
        if file == 'dir':
            exp_list += esc_codes['set_blue']
        # last position
        if file == sorted(files)[len(files)-1]:
            exp_list += f'{file}' + esc_codes['reset_attributes']
        else:
            exp_list += f'{file}  ' + esc_codes['reset_attributes']

    p.sendline(cmd)
    p.expect(cmd + EOL + exp_list + EOL + PROMPT)


def assert_ls_d(p):
    cmd = 'ls -d testDir'
    exp_list = esc_codes['set_blue'] + 'testDir' + esc_codes['reset_attributes']
    p.sendline(cmd)
    p.expect(cmd + EOL + exp_list + EOL + PROMPT)


def assert_ls_d_noarg(p):
    cmd = 'ls -d'
    exp_list = esc_codes['set_blue'] \
        + '.' \
        + esc_codes['reset_attributes']

    p.sendline(cmd)
    p.expect(cmd + EOL + exp_list + EOL + PROMPT)


def assert_ls_f(p, files):
    cmd = 'ls -f testDir'
    exp_list = ''
    for file in files:
        if file == 'dir':
            exp_list += esc_codes['set_blue']
        if file[0] == '.':
            continue
        # last position
        if file == files[len(files)-1]:
            exp_list += f'{file}' + esc_codes['reset_attributes']
        else:
            exp_list += f'{file}  ' + esc_codes['reset_attributes']

    p.sendline(cmd)
    p.expect(cmd + EOL + exp_list + EOL + PROMPT)


def assert_ls_h(p):
    cmd = 'ls -h'
    ls_help = r'(usage: ls \[options\] \[files\](\r+)\n' \
              + r'  -1:  one entry per line(\r+)\n' \
              + r'  -a:  do not ignore entries starting with .(\r+)\n' \
              + r'  -d:  list directories themselves, not their contents(\r+)\n' \
              + r'  -f:  do not sort(\r+)\n' \
              + r'  -h:  prints help(\r+)\n' \
              + r'  -l:  long listing format(\r+)\n' \
              + r'  -r:  sort in reverse order(\r+)\n' \
              + r'  -S:  sort by file size, largest first(\r+)\n' \
              + r'  -t:  sort by time, newest first)'

    p.sendline(cmd)
    p.expect(cmd + EOL + ls_help + EOL + PROMPT)


def assert_ls_l(p, files):
    cmd = 'ls -l testDir'
    p.sendline(cmd)
    p.expect(cmd)
    for file in sorted(files):
        if file[0] == '.':
            continue
        p.expect(r'(-|b|c|d|l|n|p|s|D|E|O|S)([-r][-w][-x]){3}( )'
                 + r'(\d)( )'
                 + r'(root |--- ){2}( *)'
                 + r'(\d+)( )'
                 + r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)( )'
                 + r'[1-31]( *)'
                 + r'(\d){2}(:)(\d){2}( )'
                 + r'(\x1b\[34m)?'
                 + f'{file}')

    p.expect(EOL + PROMPT)


def assert_ls_r(p, files):
    cmd = 'ls -r testDir'
    exp_list = ''
    hidd_files_nr = 1
    for file in sorted(files, reverse=True):
        if file == 'dir':
            exp_list += esc_codes['set_blue']
        if file[0] == '.':
            continue
        # last position
        if file == sorted(files, reverse=True)[len(files)-1-hidd_files_nr]:
            exp_list += f'{file}' + esc_codes['reset_attributes']
        else:
            exp_list += f'{file}  ' + esc_codes['reset_attributes']

    p.sendline(cmd)
    p.expect(cmd + EOL + exp_list + EOL + PROMPT)


def assert_ls_S(p, files):
    cmd = 'ls -S testDir'
    # dir size > empty files size
    exp_list = esc_codes['set_blue'] + 'dir  ' + esc_codes['reset_attributes']

    for file in sorted(files):
        if file == 'dir':
            continue
        if file[0] == '.':
            continue
        if file == sorted(files)[len(files)-1]:
            exp_list += f'{file}' + esc_codes['reset_attributes']
        else:
            exp_list += f'{file}  ' + esc_codes['reset_attributes']

    p.sendline(cmd)
    p.expect(cmd + EOL + exp_list + EOL + PROMPT)

# newly created files have all 'Jan 1 00:00' creation time
# so can't check if it works properly in automatic test
# def assert_ls_t(p, files):
#     cmd = 'ls -f testDir'
#     exp_list = ''
#     for file in files:
#         if file == 'dir':
#             exp_list += esc_codes['set_blue']
#         if file[0] == '.':
#             continue
#         # last position
#         if file == files[len(files)-1]:
#             exp_list += f'{file}' + esc_codes['reset_attributes']
#         else:
#             exp_list += f'{file}  ' + esc_codes['reset_attributes']

#     p.sendline(cmd)
#     p.expect(cmd + EOL + exp_list + EOL + PROMPT)


def assert_ls_devcolor(p):
    cmd = 'ls dev'
    # the following regex will match list of various devices
    exp_list = f'(({esc_codes["set_yellowonblack"]}' \
               + r'(\S+)[ \t]*' \
               + f'{esc_codes["reset_attributes"]}' \
               + r')+' \
               + EOL \
               + r')+'

    p.sendline(cmd)
    p.expect(exp_list + PROMPT)


def assert_ls_execolor(p):
    if is_hardware_target(p):
        cmd = 'ls syspage'
    else:
        cmd = 'ls bin'

    p.sendline(cmd)
    # assume that ls binary is in directory with binaries
    p.expect(esc_codes['set_green'] + 'psh')
    p.expect(PROMPT)


def assert_ls_pshcmds(p):
    cmd = 'ls bin'

    p.sendline(cmd)
    assert_allfiles_occurence(p, PSH_COMMANDS)


def harness(p):
    # that array shouldn't be changed for the tests to working properly
    files = ['.hidden', 'test1', 'test0', 'dir']

    run_psh(p)
    assert_only_prompt(p)

    create_testdir(p)
    create_testfiles(p, files)
    create_intdir(p)

    assert_ls_err(p)
    assert_ls_noarg(p, files)
    assert_ls_1(p, files)
    assert_ls_a(p, files)
    assert_ls_d(p)
    # temporarily disabled in order to show ls_pshcmds fail
    # assert_ls_d_noarg(p)
    assert_ls_f(p, files)
    assert_ls_h(p)
    assert_ls_l(p, files)
    assert_ls_r(p, files)
    assert_ls_S(p, files)
    assert_ls_devcolor(p)
    # on imxrt106x target psh cmds links and executables colors aren't visible
    if not is_hardware_target(p):
        assert_ls_execolor(p)
        assert_ls_pshcmds(p)

    return True

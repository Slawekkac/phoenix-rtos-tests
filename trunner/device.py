# Imports of available runners
from .runners import HostRunner, QemuRunner, IMXRT106xRunner, IMXRT117xRunner

from .config import PHRTOS_PROJECT_DIR, SERIAL_DEVICES, USB_ADDRESSES



QEMU_CMD = {
    'ia32-generic': (
        'qemu-system-i386',
        [
            '-hda', f'{PHRTOS_PROJECT_DIR}/_boot/phoenix-ia32-generic.disk',
            '-nographic',
            '-monitor', 'none'
        ]
    )
}


class RunnerFactory:
    @staticmethod
    def create(target):
        if target == 'ia32-generic':
            return QemuRunner(*QEMU_CMD[target])
        if target == 'host-pc':
            return HostRunner()
        if target == 'armv7m7-imxrt106x':
            return IMXRT106xRunner(SERIAL_DEVICES.get(target), USB_ADDRESSES.get(target))
        if target == 'armv7m7-imxrt117x':
            return IMXRT117xRunner(SERIAL_DEVICES.get(target))

        raise ValueError(f"Unknown Runner target: {target}")

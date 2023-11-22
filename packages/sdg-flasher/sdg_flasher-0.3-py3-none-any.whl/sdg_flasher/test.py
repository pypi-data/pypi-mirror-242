
from sdg_io import SdgIO
from sdg_utils import log_init, DEBUG
from __init__ import Flasher
import os

PATH = 'j:/Project/OTHER/stm32f4_tmpl/bin'
file = f'{PATH}/stm32f4_tmpl.hex'


if __name__ == '__main__':
    log = log_init()
    log.setLevel(DEBUG)
    io = SdgIO('COM7', '500000_O_1', log=log)
    flasher = Flasher(io,
                      filename=file,
                      device='stm32f4',
                      opt='wv',
                      addr=b'\x01',
                      reboot=b'\x00',
                      log=log)
    flasher.do()
    # flasher.send_fullerase()


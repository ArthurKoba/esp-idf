# SPDX-FileCopyrightText: 2022-2025 Espressif Systems (Shanghai) CO LTD
# SPDX-License-Identifier: Unlicense OR CC0-1.0
import logging
import re

import pytest
from pytest_embedded import Dut
from pytest_embedded_idf.utils import idf_parametrize


@pytest.mark.temp_skip_ci(targets=['esp32c61'], reason='C5 C61 GPSPI same, so testing on C5 is enough')
@pytest.mark.sdcard_spimode
@idf_parametrize('target', ['esp32', 'esp32s3', 'esp32c3', 'esp32p4', 'esp32c5'], indirect=['target'])
def test_examples_sd_card_sdspi(dut: Dut) -> None:
    dut.expect('example: Initializing SD card', timeout=20)
    dut.expect('example: Using SPI peripheral', timeout=20)

    # Provide enough time for possible SD card formatting
    dut.expect('Filesystem mounted', timeout=180)

    # These lines are matched separately because of ASCII color codes in the output
    name = dut.expect(re.compile(rb'Name: (\w+)\r'), timeout=20).group(1).decode()
    _type = dut.expect(re.compile(rb'Type: (\S+)'), timeout=20).group(1).decode()
    speed = dut.expect(re.compile(rb'Speed: (\S+)'), timeout=20).group(1).decode()
    size = dut.expect(re.compile(rb'Size: (\S+)'), timeout=20).group(1).decode()

    logging.info('Card {} {} {}MHz {} found'.format(name, _type, speed, size))

    message_list1 = (
        'Opening file /sdcard/hello.txt',
        'File written',
        'Renaming file /sdcard/hello.txt to /sdcard/foo.txt',
        'Reading file /sdcard/foo.txt',
        "Read from file: 'Hello {}!'".format(name),
    )
    sd_card_format = re.compile(str.encode('Formatting card, allocation unit size=\\S+'))
    message_list2 = (
        "file doesn't exist, formatting done",
        'Opening file /sdcard/nihao.txt',
        'File written',
        'Reading file /sdcard/nihao.txt',
        "Read from file: 'Nihao {}!'".format(name),
        'Card unmounted',
    )

    for msg in message_list1:
        dut.expect_exact(msg, timeout=30)
    dut.expect(sd_card_format, timeout=180)  # Provide enough time for SD card FATFS format operation
    for msg in message_list2:
        dut.expect_exact(msg, timeout=180)

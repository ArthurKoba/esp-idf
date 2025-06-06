# SPDX-FileCopyrightText: 2023-2025 Espressif Systems (Shanghai) CO LTD
# SPDX-License-Identifier: CC0-1.0
import pytest
from pytest_embedded import Dut
from pytest_embedded_idf.utils import idf_parametrize


@pytest.mark.generic
@pytest.mark.parametrize(
    'config',
    [
        'intl',
        'ext',
    ],
    indirect=True,
)
@idf_parametrize('target', ['esp32h2', 'esp32p4', 'esp32c5', 'esp32c61'], indirect=['target'])
def test_ana_cmpr_example(dut: Dut) -> None:
    sdkconfig = dut.app.sdkconfig
    dut.expect(
        r'ana_cmpr_example: Analog Comparator source gpio ([0-9]+), external reference gpio ([0-9]+)', timeout=10
    )
    if sdkconfig['EXAMPLE_INTERNAL_REF']:
        dut.expect('ana_cmpr_example: Allocate Analog Comparator with internal reference', timeout=10)
        dut.expect(r'ana_cmpr_example: Analog comparator enabled, reference voltage: [0-9]+% \* VDD', timeout=10)
    elif sdkconfig['EXAMPLE_EXTERNAL_REF']:
        dut.expect('ana_cmpr_example: Allocate Analog Comparator with external reference', timeout=10)
        dut.expect('ana_cmpr_example: Analog comparator enabled, external reference selected', timeout=10)

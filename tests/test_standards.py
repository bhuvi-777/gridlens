import pandas as pd

from gridlens.standards import (
    check_en50160,
    check_ieee519_voltage,
)


def interval_frame(offset=1.0, thd=0.0, h5=0.0, count=100):
    return pd.DataFrame({
        "start": [600 * i for i in range(count)],
        "urms": [230 * offset] * count,
        "freq": [50.0] * count,
        "thd": [thd] * count,
        "h5": [h5] * count,
        **{f"h{order}": [0.0] * count for order in range(2, 41) if order != 5},
    })


def test_clean_en50160_passes():
    result = check_en50160(interval_frame())
    assert result.passed
    assert "indicative only" in result.summary()


def test_voltage_offset_fails_en50160():
    result = check_en50160(interval_frame(offset=1.12))
    voltage_check = next(c for c in result.checks if c.name == "Supply voltage +/-10%")
    assert not voltage_check.passed


def test_thd_fails_en50160():
    result = check_en50160(interval_frame(thd=9.0))
    thd_check = next(c for c in result.checks if c.name == "Voltage THD")
    assert not thd_check.passed


def test_harmonic_fails_with_order_name():
    result = check_en50160(interval_frame(h5=7.0))
    check = next(c for c in result.checks if c.name == "Harmonic h5")
    assert not check.passed


def test_ieee519_bus_classes():
    low = check_ieee519_voltage(interval_frame(thd=7.0, h5=4.0), 0.4)
    medium = check_ieee519_voltage(interval_frame(thd=4.0, h5=2.0), 69)
    assert low.passed
    assert medium.passed
    fail = check_ieee519_voltage(interval_frame(thd=6.0, h5=4.0), 69)
    assert not fail.passed

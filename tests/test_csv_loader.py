import numpy as np
import pandas as pd
import pytest

from gridlens.generator import sine_wave
from gridlens.loaders import load_csv


def test_load_csv_with_time_column(tmp_path):
    t, v = sine_wave()
    path = tmp_path / "capture.csv"
    pd.DataFrame({"time": t, "voltage": v}).to_csv(path, index=False)

    wave = load_csv(path)

    assert wave.fs == pytest.approx(10_000)
    assert np.allclose(wave.voltage, v)
    assert wave.current is None


def test_load_csv_with_current_and_fs(tmp_path):
    _, v = sine_wave(rms=230.0)
    _, i = sine_wave(rms=10.0)
    path = tmp_path / "capture.csv"
    pd.DataFrame({"v": v, "i": i}).to_csv(path, index=False)

    wave = load_csv(path, voltage_col="v", current_col="i", fs=10_000)

    assert wave.fs == pytest.approx(10_000)
    assert wave.current is not None
    assert np.allclose(wave.current, i)


def test_missing_voltage_column_raises(tmp_path):
    path = tmp_path / "bad.csv"
    path.write_text("a,b\n1,2\n")
    with pytest.raises(KeyError):
        load_csv(path)


def test_no_time_and_no_fs_raises(tmp_path):
    path = tmp_path / "no_time.csv"
    path.write_text("voltage\n1\n2\n3\n")
    with pytest.raises(ValueError):
        load_csv(path)
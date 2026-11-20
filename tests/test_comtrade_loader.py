from pathlib import Path

import pytest

from gridlens.loaders import load_comtrade


def test_comtrade_optional_loader(tmp_path: Path):
    pytest.importorskip("comtrade")
    cfg = tmp_path / "sample.cfg"
    dat = tmp_path / "sample.dat"
    cfg.write_text(
        "station,record,1999\n"
        "1,1A,0D\n"
        "1,VA1,,,V,1.0,0.0,0.0,-32767,32767,1.0,1.0,P\n"
        "50\n"
        "1\n"
        "1000,1\n"
        "01/01/2020,00:00:00.000000\n"
        "01/01/2020,00:00:00.000000\n"
        "ASCII\n"
        "1\n",
        encoding="ascii",
    )
    dat.write_text("1,0,1000\n", encoding="ascii")
    wave = load_comtrade(cfg, voltage_channel="VA1")
    assert wave.voltage.size > 0
    assert wave.voltage[0] == 1000.0

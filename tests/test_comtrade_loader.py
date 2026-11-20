from pathlib import Path

import pytest

from gridlens.loaders import load_comtrade


def test_comtrade_optional_loader(tmp_path: Path):
    pytest.importorskip("comtrade")
    cfg = tmp_path / "sample.cfg"
    dat = tmp_path / "sample.dat"
    cfg.write_text(
        "station,record,1999\n"
        "1,1,60\n"
        "1,1\n"
        "VA1,Voltage, ,V,1.0,0.0,0.0,-32767,32767\n"
        "1\n"
        "50\n",
        encoding="ascii",
    )
    dat.write_text("1,0,1000,0\n", encoding="ascii")
    wave = load_comtrade(cfg)
    assert wave.voltage.size > 0

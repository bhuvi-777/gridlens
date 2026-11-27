import numpy as np

from gridlens.waveform import Waveform, resample


def test_resample_preserves_waveform_start_time():
    start = 5.0
    t = start + np.arange(1_000) / 10_000
    wave = Waveform(t=t, voltage=np.sin(2 * np.pi * 50 * t))

    result = resample(wave, 5_000)

    assert result.t[0] == start
    np.testing.assert_allclose(
        result.t, start + np.arange(500) / 5_000, rtol=0, atol=1e-12
    )

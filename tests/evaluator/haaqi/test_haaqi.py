"""Tests for haaqi module"""
import numpy as np
import pytest

from clarity.evaluator.haaqi import compute_haaqi, haaqi_v1
from clarity.evaluator.msbg.audiogram import Audiogram


def test_haaqi_v1() -> None:
    """Test for haaqi_v1 index"""
    np.random.seed(0)
    sample_rate = 16000
    x = np.random.uniform(-1, 1, int(sample_rate * 0.5))  # i.e. 500 ms of audio
    y = np.random.uniform(-1, 1, int(sample_rate * 0.5))

    hearing_loss = np.array([45, 45, 35, 45, 60, 65])
    equalisation_mode = 1
    level1 = 65

    score, _, _, _ = haaqi_v1(
        x, sample_rate, y, sample_rate, hearing_loss, equalisation_mode, level1
    )
    assert score == pytest.approx(
        0.111290948, rel=pytest.rel_tolerance, abs=pytest.abs_tolerance
    )


@pytest.mark.parametrize(
    "scale_reference,expected_result",
    [(False, 0.113759275), (True, 0.114157435)],
)
def test_compute_haaqi(scale_reference, expected_result):
    """Test for compute_haaqi function"""
    np.random.seed(42)

    sample_rate = 16000
    enh_signal = np.random.uniform(-1, 1, int(sample_rate * 0.5))
    ref_signal = np.random.uniform(-1, 1, int(sample_rate * 0.5))

    audiogram = Audiogram(
        levels=np.array([10, 20, 30, 40, 50, 60]),
        frequencies=np.array([250, 500, 1000, 2000, 4000, 6000]),
    )

    # Compute HAAQI score
    score = compute_haaqi(
        processed_signal=enh_signal,
        reference_signal=ref_signal,
        audiogram=audiogram,
        sample_rate=sample_rate,
        scale_reference=scale_reference,
    )

    # Check that the score is a float between 0 and 1
    assert score == pytest.approx(
        expected_result, rel=pytest.rel_tolerance, abs=pytest.abs_tolerance
    )

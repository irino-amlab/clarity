"""Tests for hasqi module"""
import numpy as np
import pytest

from clarity.evaluator.hasqi import hasqi_v2, hasqi_v2_better_ear
from clarity.evaluator.msbg.audiogram import Audiogram


def test_hasqi_v2() -> None:
    """Test for hasqi_v2 index"""
    np.random.seed(0)
    sample_rate = 16000
    x = np.random.uniform(-1, 1, int(sample_rate * 0.5))  # i.e. 500 ms of audio
    y = np.random.uniform(-1, 1, int(sample_rate * 0.5))

    hearing_loss = np.array([45, 45, 35, 45, 60, 65])
    equalisation_mode = 1
    level1 = 65

    score, _, _, _ = hasqi_v2(
        x, sample_rate, y, sample_rate, hearing_loss, equalisation_mode, level1
    )
    assert score == pytest.approx(
        0.002525809, rel=pytest.rel_tolerance, abs=pytest.abs_tolerance
    )


def test_hasqi_v2_better_ear() -> None:
    """Test for hasqi_v2_better_ear index"""

    np.random.seed(0)
    sample_rate = 16000

    freqs = np.array([250, 500, 1000, 2000, 4000, 6000])
    audiogram_left = Audiogram(
        levels=np.array([25, 25, 25, 25, 40, 65]), frequencies=freqs
    )
    audiogram_right = Audiogram(
        levels=np.array([45, 45, 35, 45, 60, 65]), frequencies=freqs
    )

    ref_left = np.random.uniform(-1, 1, int(sample_rate * 0.5))  # i.e. 500 ms of audio
    ref_right = np.random.uniform(-1, 1, int(sample_rate * 0.5))
    proc_left = np.random.uniform(-1, 1, int(sample_rate * 0.5))  # i.e. 500 ms of audio
    proc_right = np.random.uniform(-1, 1, int(sample_rate * 0.5))

    score = hasqi_v2_better_ear(
        reference_left=ref_left,
        reference_right=ref_right,
        processed_left=proc_left + ref_left,
        processed_right=proc_right,
        sample_rate=sample_rate,
        audiogram_left=audiogram_left,
        audiogram_right=audiogram_right,
        level=100,
    )

    assert score == pytest.approx(
        0.1256893032667640, rel=pytest.rel_tolerance, abs=pytest.abs_tolerance
    )

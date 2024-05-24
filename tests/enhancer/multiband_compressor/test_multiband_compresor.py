import numpy as np
import pytest

from clarity.enhancer.multiband_compressor.compressor_qmul import Compressor
from clarity.enhancer.multiband_compressor.multiband_compressor import (
    MultibandCompressor,
)


@pytest.fixture
def default_compressor():
    return Compressor()


def test_compressor_initialization(default_compressor):
    """Test the initialization of the Compressor class."""
    assert default_compressor.threshold == 0.0
    assert default_compressor.ratio == 1.0
    assert default_compressor.attack == 15.0
    assert default_compressor.release == 100.0
    assert default_compressor.gain == 0.0
    assert default_compressor.sample_rate == 44100.0


def test_compressor_signal_processing(default_compressor):
    """Test the signal processing of the Compressor class."""
    input_signal = np.array([[1, 2, 3, 4, 5]])
    output_signal = default_compressor(input_signal)
    # Add assertions to verify the output signal
    assert isinstance(output_signal, np.ndarray)
    assert len(output_signal) == len(input_signal)
    assert np.sum(output_signal) == pytest.approx(
        15, rel=pytest.rel_tolerance, abs=pytest.abs_tolerance
    )


@pytest.fixture
def default_multiband_compressor():
    """Fixture for the MultibandCompressor class with default parameters."""
    return MultibandCompressor(
        crossover_frequencies=np.array([250, 500, 1000, 2000, 4000]) * np.sqrt(2)
    )


def test_multiband_compressor_initialization(default_multiband_compressor):
    """Test the initialization of the MultibandCompressor class."""
    assert np.sum(default_multiband_compressor.xover_freqs) == pytest.approx(
        np.sum(
            np.array(
                [
                    250,
                    500,
                    1000,
                    2000,
                    4000,
                ]
            )
            * np.sqrt(2)
        ),
        rel=pytest.rel_tolerance,
        abs=pytest.abs_tolerance,
    )

    assert np.sum(default_multiband_compressor.xover_freqs) == pytest.approx(
        np.sum(np.array(default_multiband_compressor.xover_freqs)),
        rel=pytest.rel_tolerance,
        abs=pytest.abs_tolerance,
    )
    assert default_multiband_compressor.sample_rate == 44100.0


def test_multiband_compressor_invalid_parameters():
    """Test the initialization of the MultibandCompressor class with
    invalid parameters.
    """
    with pytest.raises(ValueError):
        MultibandCompressor(crossover_frequencies=[250, 500, 1000, 2000, 4000], order=3)


def test_multiband_compressor_set_compressors(default_multiband_compressor):
    """Test the set_compressors method of the MultibandCompressor class."""
    default_multiband_compressor.set_compressors(
        attack=10.0, release=50.0, threshold=-20.0, ratio=2.0, gain=6.0
    )
    assert len(default_multiband_compressor.compressor) == 6


def test_multiband_compressor_call(default_multiband_compressor):
    """Test the __call__ method of the MultibandCompressor class."""
    signal = np.random.rand(1000)
    signal = signal[np.newaxis, :]

    default_multiband_compressor.set_compressors()
    compressed_signal = default_multiband_compressor(signal)
    assert isinstance(compressed_signal, np.ndarray)


def test_multiband_compressor_str(default_multiband_compressor):
    """Test the __str__ method of the MultibandCompressor class."""
    summary_text = str(default_multiband_compressor)
    assert "Multiband Compressor Summary:" in summary_text

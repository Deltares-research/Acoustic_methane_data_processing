import pytest

from acoustic_methane.read_raw_data import process_raw_file


def test_process_raw_file_requires_existing_input(tmp_path):
    with pytest.raises(FileNotFoundError, match="Raw sonar file does not exist"):
        process_raw_file(tmp_path / "missing.raw", tmp_path / "output")


def test_process_raw_file_rejects_nonpositive_plot_duration(tmp_path):
    with pytest.raises(ValueError, match="plot_duration_minutes"):
        process_raw_file(
            tmp_path / "missing.raw",
            tmp_path / "output",
            plot_duration_minutes=0,
        )


@pytest.mark.parametrize(
    "range_limits",
    [(1.0, 1.0), (3.0, 1.0), (float("-inf"), 1.0)],
)
def test_process_raw_file_rejects_invalid_range_limits(tmp_path, range_limits):
    with pytest.raises(ValueError, match="range_limits_m"):
        process_raw_file(
            tmp_path / "missing.raw",
            tmp_path / "output",
            range_limits_m=range_limits,
        )

from pathlib import Path

import pytest

from acoustic_methane.pipeline import discover_raw_files, run_pipeline
from acoustic_methane.read_raw_data import ProcessingResult


def test_run_pipeline_processes_raw_files_recursively_in_order(tmp_path, monkeypatch):
    raw_dir = tmp_path / "raw"
    nested_dir = raw_dir / "nested"
    nested_dir.mkdir(parents=True)
    first_file = raw_dir / "a.raw"
    nested_file = nested_dir / "B.RAW"
    ignored_file = raw_dir / "notes.txt"
    first_file.touch()
    nested_file.touch()
    ignored_file.touch()

    calls = []

    def fake_process_raw_file(raw_file, output_dir, **options):
        calls.append((Path(raw_file), Path(output_dir), options))
        return ProcessingResult(
            converted_file=Path(output_dir) / f"{Path(raw_file).stem}.nc",
            sv_plot=Path(output_dir) / f"{Path(raw_file).stem}_Sv_plot.png",
        )

    monkeypatch.setattr(
        "acoustic_methane.pipeline.process_raw_file", fake_process_raw_file
    )
    output_dir = tmp_path / "processed"
    result = run_pipeline(
        {
            "paths": {
                "raw_data": str(raw_dir),
                "processed_data": str(output_dir),
            }
        }
    )

    assert result["status"] == "ok"
    assert result["files_processed"] == 2
    assert [call[0] for call in calls] == [first_file, nested_file]
    assert all(call[1] == output_dir for call in calls)
    assert all(call[2]["waveform_mode"] == "BB" for call in calls)
    assert output_dir.is_dir()


def test_run_pipeline_requires_raw_files(tmp_path):
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()
    with pytest.raises(FileNotFoundError, match="No .raw files found"):
        run_pipeline(
            {
                "paths": {
                    "raw_data": str(raw_dir),
                    "processed_data": str(tmp_path / "processed"),
                }
            }
        )


def test_run_pipeline_rejects_invalid_range_configuration(tmp_path):
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()
    (raw_dir / "sample.raw").touch()
    with pytest.raises(ValueError, match="range_limits_m"):
        run_pipeline(
            {
                "paths": {
                    "raw_data": str(raw_dir),
                    "processed_data": str(tmp_path / "processed"),
                },
                "raw_processing": {"range_limits_m": [0.0]},
            }
        )


def test_run_pipeline_processes_experiment_ek80_layout(tmp_path, monkeypatch):
    raw_dir = tmp_path / "raw"
    day_a = raw_dir / "day_a"
    day_b = raw_dir / "day_b"
    (day_a / "something_ek80").mkdir(parents=True)
    (day_b / "something_ek80").mkdir(parents=True)
    first_day_raw = day_a / "something_ek80" / "a_first.raw"
    second_day_raw = day_b / "something_ek80" / "b_first.raw"
    first_day_raw.touch()
    second_day_raw.touch()

    calls = []

    def fake_process_raw_file(raw_file, output_dir, **options):
        calls.append((Path(raw_file), Path(output_dir), options))
        return ProcessingResult(
            converted_file=Path(output_dir) / f"{Path(raw_file).stem}.nc",
            sv_plot=Path(output_dir) / f"{Path(raw_file).stem}_Sv_plot.png",
        )

    monkeypatch.setattr(
        "acoustic_methane.pipeline.process_raw_file", fake_process_raw_file
    )
    output_dir = tmp_path / "processed"
    result = run_pipeline(
        {
            "paths": {
                "raw_data": str(raw_dir),
                "processed_data": str(output_dir),
            },
            "raw_processing": {"discovery_mode": "experiment_ek80"},
        }
    )

    assert result["status"] == "ok"
    assert result["files_processed"] == 2
    assert [call[0] for call in calls] == [first_day_raw, second_day_raw]


def test_run_pipeline_requires_ek80_directory_in_experiment_layout(tmp_path):
    raw_dir = tmp_path / "raw"
    (raw_dir / "day_a").mkdir(parents=True)
    with pytest.raises(FileNotFoundError, match=r"\*_ek80"):
        run_pipeline(
            {
                "paths": {
                    "raw_data": str(raw_dir),
                    "processed_data": str(tmp_path / "processed"),
                },
                "raw_processing": {"discovery_mode": "experiment_ek80"},
            }
        )


def test_discover_raw_files_does_not_require_processed_output_path(tmp_path):
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()
    raw_file = raw_dir / "example.raw"
    raw_file.touch()

    discovered = discover_raw_files({"paths": {"raw_data": str(raw_dir)}})

    assert discovered == [raw_file]

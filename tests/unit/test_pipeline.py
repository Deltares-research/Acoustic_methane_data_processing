from pathlib import Path

import pytest

from acoustic_methane.pipeline import run_pipeline
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

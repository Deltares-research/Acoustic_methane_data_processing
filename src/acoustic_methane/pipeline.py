"""Batch processing pipeline for raw sonar files."""

from pathlib import Path
from typing import Any

from acoustic_methane.read_raw_data import process_raw_file


def run_pipeline(config: dict[str, Any]) -> dict[str, Any]:
    """Process every configured raw sonar file and return generated output paths.

    Raw files are discovered recursively by default and processed in
    case-insensitive, deterministic path order. Processing stops and raises if
    a file cannot be converted or plotted.
    """
    paths = config.get("paths")
    if not isinstance(paths, dict):
        raise ValueError("Pipeline config must contain a 'paths' mapping.")

    raw_data_value = paths.get("raw_data")
    processed_data_value = paths.get("processed_data")
    if not isinstance(raw_data_value, (str, Path)) or not str(raw_data_value).strip():
        raise ValueError("'paths.raw_data' must be a non-empty directory path.")
    if not isinstance(processed_data_value, (str, Path)) or not str(
        processed_data_value
    ).strip():
        raise ValueError("'paths.processed_data' must be a non-empty directory path.")

    raw_dir = Path(raw_data_value)
    if not raw_dir.is_dir():
        raise FileNotFoundError(f"Raw-data directory does not exist: {raw_dir}")

    raw_processing = config.get("raw_processing", {})
    if not isinstance(raw_processing, dict):
        raise ValueError("'raw_processing' must be a mapping.")

    recursive = raw_processing.get("recursive", True)
    if not isinstance(recursive, bool):
        raise ValueError("'raw_processing.recursive' must be true or false.")

    raw_files = raw_dir.rglob("*") if recursive else raw_dir.iterdir()
    files_to_process = sorted(
        (
            path
            for path in raw_files
            if path.is_file() and path.suffix.casefold() == ".raw"
        ),
        key=lambda path: str(path).casefold(),
    )
    if not files_to_process:
        raise FileNotFoundError(f"No .raw files found in {raw_dir}")

    range_limits = raw_processing.get("range_limits_m", (0.0, 10.0))
    if not isinstance(range_limits, (list, tuple)) or len(range_limits) != 2:
        raise ValueError(
            "'raw_processing.range_limits_m' must contain minimum and maximum values."
        )

    options = {
        "channel": raw_processing.get("channel"),
        "sonar_model": raw_processing.get("sonar_model", "EK80"),
        "waveform_mode": raw_processing.get("waveform_mode", "BB"),
        "encode_mode": raw_processing.get("encode_mode", "complex"),
        "plot_duration_minutes": raw_processing.get("plot_duration_minutes", 12),
        "range_limits_m": (range_limits[0], range_limits[1]),
    }

    output_dir = Path(processed_data_value)
    results: list[dict[str, str]] = []
    for raw_file in files_to_process:
        result = process_raw_file(raw_file, output_dir, **options)
        results.append(
            {
                "raw_file": str(raw_file),
                "converted_file": str(result.converted_file),
                "sv_plot": str(result.sv_plot),
            }
        )

    return {
        "status": "ok",
        "files_processed": len(results),
        "results": results,
    }

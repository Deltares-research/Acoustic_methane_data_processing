"""Convert an EK80 raw file, calculate volume backscattering strength, and plot it."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


@dataclass(frozen=True)
class ProcessingResult:
    """Paths produced while processing one raw sonar file."""

    converted_file: Path
    sv_plot: Path


def process_raw_file(
    raw_path: str | Path,
    output_dir: str | Path,
    *,
    channel: str | None = None,
    sonar_model: str = "EK80",
    waveform_mode: str = "BB",
    encode_mode: str = "complex",
    plot_duration_minutes: int = 12,
    range_limits_m: tuple[float, float] = (0.0, 3.0),
) -> ProcessingResult:
    """Convert and calibrate a raw sonar file, then save an Sv plot.

    Args:
        raw_path: Path to the raw sonar file.
        output_dir: Directory where the NetCDF file and plot will be saved.
        channel: Optional channel to plot. If omitted, all channels are plotted.
        sonar_model: Sonar model passed to Echopype.
        waveform_mode: Waveform mode passed to the Sv calibration.
        encode_mode: Encoding mode passed to the Sv calibration.
        plot_duration_minutes: Duration from the first ping shown in the plot.
        range_limits_m: Minimum and maximum plotted range in meters.

    Returns:
        Paths to the converted NetCDF file and saved Sv plot.

    Raises:
        FileNotFoundError: If ``raw_path`` does not point to a file.
        ValueError: If plot settings are invalid or ``channel`` is unavailable.
        ImportError: If the Echopype plotting or processing dependencies are missing.
    """
    from math import isfinite

    if plot_duration_minutes <= 0:
        raise ValueError("plot_duration_minutes must be greater than zero.")

    range_min, range_max = range_limits_m
    if not (isfinite(range_min) and isfinite(range_max) and range_min < range_max):
        raise ValueError("range_limits_m must contain finite values in ascending order.")

    source_path = Path(raw_path)
    if not source_path.is_file():
        raise FileNotFoundError(f"Raw sonar file does not exist: {source_path}")

    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)

    from importlib import import_module

    import echopype as ep
    import matplotlib.pyplot as plt
    import numpy as np

    import_module("echopype.colormap")

    echodata = ep.open_raw(str(source_path), sonar_model=sonar_model)
    converted_path = destination / f"{source_path.stem}.nc"
    echodata.to_netcdf(save_path=str(converted_path))

    sv_dataset = ep.calibrate.compute_Sv(
        echodata,
        waveform_mode=waveform_mode,
        encode_mode=encode_mode,
    )
    channels = [str(value) for value in sv_dataset["channel"].values]
    if channel is not None and channel not in channels:
        available_channels = ", ".join(channels)
        raise ValueError(
            f"Channel {channel!r} is not present in the calibrated data. "
            f"Available channels: {available_channels}"
        )

    range_values = sv_dataset["echo_range"].isel(ping_time=0, channel=0).data
    sv_dataset = sv_dataset.assign_coords(
        range=("range_sample", range_values)
    ).swap_dims({"range_sample": "range"})
    sv_dataset["range"] = sv_dataset["range"].assign_attrs(
        {"long_name": "range", "units": "meter"}
    )

    sv_data = sv_dataset["Sv"]
    plot_options: dict[str, object] = {
        "x": "ping_time",
        "vmin": -80,
        "vmax": 80,
        "figsize": (12, 4),
        "cmap": "ep.ek500",
        "yincrease": False,
    }
    if channel is None:
        plot_options["row"] = "channel"
    else:
        sv_data = sv_data.sel(channel=channel, drop=True)

    sv_data.plot(**plot_options)

    figure = plt.gcf()
    start_time = sv_dataset["ping_time"].min().values
    end_time = start_time + np.timedelta64(plot_duration_minutes, "m")
    for axis in figure.axes:
        axis.set_ylim(range_max, range_min)
        axis.set_xlim(start_time, end_time)

    plot_path = destination / f"{source_path.stem}_Sv_plot.png"
    figure.savefig(plot_path, bbox_inches="tight")
    plt.close(figure)

    return ProcessingResult(converted_file=converted_path, sv_plot=plot_path)


def main(argv: Sequence[str] | None = None) -> int:
    """Run raw-file processing from the command line."""
    parser = argparse.ArgumentParser(
        description="Convert an EK80 raw file and create an Sv plot."
    )
    parser.add_argument("raw_file", type=Path, help="Path to the raw sonar file.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/processed"),
        help="Directory for converted data and the plot (default: outputs/processed).",
    )
    parser.add_argument(
        "--channel",
        help="Optional channel to plot. By default, all channels are plotted.",
    )
    parser.add_argument(
        "--sonar-model",
        default="EK80",
        help="Sonar model understood by Echopype (default: EK80).",
    )
    parser.add_argument(
        "--waveform-mode",
        default="BB",
        help="Waveform mode for calibration (default: BB).",
    )
    parser.add_argument(
        "--encode-mode",
        default="complex",
        help="Encoding mode for calibration (default: complex).",
    )
    parser.add_argument(
        "--plot-duration-minutes",
        type=int,
        default=12,
        help="Minutes from the first ping to include in the plot (default: 12).",
    )
    parser.add_argument(
        "--range-limits-m",
        nargs=2,
        type=float,
        metavar=("MIN", "MAX"),
        default=(0.0, 3.0),
        help="Minimum and maximum plotted range in meters (default: 0 3).",
    )
    args = parser.parse_args(argv)

    result = process_raw_file(
        args.raw_file,
        args.output_dir,
        channel=args.channel,
        sonar_model=args.sonar_model,
        waveform_mode=args.waveform_mode,
        encode_mode=args.encode_mode,
        plot_duration_minutes=args.plot_duration_minutes,
        range_limits_m=(args.range_limits_m[0], args.range_limits_m[1]),
    )
    print(f"Converted data: {result.converted_file}")
    print(f"Sv plot: {result.sv_plot}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

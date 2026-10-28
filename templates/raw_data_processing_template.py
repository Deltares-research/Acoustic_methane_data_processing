"""Editable settings template for processing one raw sonar file."""

from pathlib import Path

from acoustic_methane.read_raw_data import process_raw_file


# Replace these values with the paths and channel for your own data.
RAW_FILE = Path(r"data\raw\your_sonar_file.raw")
OUTPUT_DIR = Path(r"outputs\processed")
CHANNEL: str | None = None  # Set a channel name to plot only that channel.


def main() -> None:
    """Run the processor with the settings above."""
    result = process_raw_file(
        raw_path=RAW_FILE,
        output_dir=OUTPUT_DIR,
        channel=CHANNEL,
        sonar_model="EK80",
        waveform_mode="BB",
        encode_mode="complex",
        plot_duration_minutes=12,
        range_limits_m=(0.0, 3.0),
    )
    print(f"Converted data: {result.converted_file}")
    print(f"Sv plot: {result.sv_plot}")


if __name__ == "__main__":
    main()

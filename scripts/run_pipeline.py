from pathlib import Path
import argparse

from acoustic_methane.config import load_config
from acoustic_methane.pipeline import discover_raw_files, run_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Run acoustic methane processing pipeline")
    parser.add_argument("--config", type=Path, required=True, help="Path to YAML config")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List discovered raw files and exit without processing.",
    )
    args = parser.parse_args()

    cfg = load_config(args.config)
    if args.dry_run:
        discovered_files = discover_raw_files(cfg)
        print(f"Discovered {len(discovered_files)} raw file(s):")
        for raw_file in discovered_files:
            print(f"  {raw_file}")
        return

    result = run_pipeline(cfg)
    print(f"Processed {result['files_processed']} raw file(s):")
    for item in result["results"]:
        print(f"  Raw file: {item['raw_file']}")
        print(f"  NetCDF:   {item['converted_file']}")
        print(f"  Sv plot:  {item['sv_plot']}")


if __name__ == "__main__":
    main()

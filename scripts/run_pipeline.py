from pathlib import Path
import argparse

from acoustic_methane.config import load_config
from acoustic_methane.pipeline import run_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Run acoustic methane processing pipeline")
    parser.add_argument("--config", type=Path, required=True, help="Path to YAML config")
    args = parser.parse_args()

    cfg = load_config(args.config)
    result = run_pipeline(cfg)
    print(f"Processed {result['files_processed']} raw file(s):")
    for item in result["results"]:
        print(f"  Raw file: {item['raw_file']}")
        print(f"  NetCDF:   {item['converted_file']}")
        print(f"  Sv plot:  {item['sv_plot']}")


if __name__ == "__main__":
    main()

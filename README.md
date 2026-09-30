# Acoustic Methane Data Processing

Repository for processing acoustic sonar data and detecting methane bubble activity.

## Structure

```
src/acoustic_methane/   Core processing code
scripts/                Pipeline entrypoint
notebooks/              Analysis notebooks
configs/                Runtime configuration
data/                   raw/interim/processed/sample
outputs/                figures/tables/reports
tests/                  Minimal automated checks
```

## Quick Start

1. Create and activate your preferred Python environment.
2. Install dependencies:

   ```bash
   pip install -r requirements/dev.txt
   pip install -e .
   ```

3. Run the pipeline skeleton:

   ```bash
   python scripts/run_pipeline.py --config configs/default.yaml
   ```

## Data Policy

- Do not commit large or sensitive raw data.
- Keep only small sample datasets in `data/sample/`.


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

3. Put your `.raw` sonar files in the configured raw-data folder. By default,
   the pipeline searches `data/raw` recursively and writes the NetCDF files and
   Sv plots to `data/processed`.
4. Run the pipeline:

   ```bash
   python scripts/run_pipeline.py --config configs/default.yaml
   ```

   Update `paths.raw_data` and `paths.processed_data` in the YAML file to use
   different folders. The `raw_processing` section configures recursive
   discovery and calibration/plot settings. Processing stops on the first file
   that fails, and reports the error rather than silently skipping it.

## Processing a Raw Sonar File

The raw-data reader can be run as a command-line tool:

```powershell
python -m acoustic_methane.read_raw_data path\to\sonar_file.raw `
  --output-dir outputs\processed `
  --channel "WBT Tube 291337-15 ES120-7CD_ES"
```

Omit `--channel` to plot all channels. The command writes a NetCDF conversion and
an Sv plot to the output directory. For a reusable starting point, see
[templates/README.md](templates/README.md).

## Data Policy

- Do not commit large or sensitive raw data.
- Keep only small sample datasets in `data/sample/`.

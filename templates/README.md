# Raw-data processing template

Use [`raw_data_processing_template.py`](./raw_data_processing_template.py) as a
small, editable entry point. The processing logic stays in
`acoustic_methane.read_raw_data`; the template contains the settings you will
usually change.

## Set it up

From the repository root, create and activate a Python environment, then install
the project and its development tools:

```powershell
python -m pip install -r requirements\dev.txt
python -m pip install -e .
```

## Adapt it

1. Open `templates/raw_data_processing_template.py`.
2. Set `RAW_FILE` to the path of your raw sonar file.
3. Set `OUTPUT_DIR` to where you want the NetCDF conversion and plot saved.
4. Leave `CHANNEL = None` to plot every channel, or set it to an exact channel
   name in the raw file.
5. Adjust `sonar_model`, `waveform_mode`, and `encode_mode` if your sonar or
   acquisition settings differ.
6. Adjust `plot_duration_minutes` and `range_limits_m` for the plot you need.

Run the template from the repository root:

```powershell
python templates\raw_data_processing_template.py
```

The output directory is created if needed. The input file must exist and the
requested channel must be present in the calibrated data. Keep large or
sensitive raw files out of version control; see the data policy in the root
README.

## Use the command line instead

You can run the same processor without editing the template:

```powershell
python -m acoustic_methane.read_raw_data data\raw\your_sonar_file.raw `
  --output-dir outputs\processed `
  --channel "your exact channel name"
```

Run the command with `--help` to see all available processing options.

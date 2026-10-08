import warnings
from pathlib import Path
import echopype as ep  # we recommend using "ep"
import xarray as xr
import hvplot.xarray  # for interactive plots
import matplotlib.pyplot as plt

file_name_raw = "D20261001-T124128.raw"
raw_path = rf"P:\11212489-008-acoustic-ch4-test\EK80\Data\{file_name_raw}"
output_path = r"P:\11212489-008-acoustic-ch4-test\data_processing\converted_files"

ed = ep.open_raw(
    raw_path,
    sonar_model="EK80",
)

filename = raw_path.split("\\")[-1].split(".")[0]
ed.to_netcdf(save_path=f"{output_path}/{filename}.nc")  # save to FILENAME.nc in the folder unpacked_files

nc_path = f'{output_path}/{filename}.nc'   # path to a converted nc file
echodata = ep.open_converted(nc_path)      # create an EchoData object

ds_Sv = ep.calibrate.compute_Sv(ed, waveform_mode="CW", encode_mode="complex")

# Plot all 3 channels for inspection
ds_Sv["Sv"].plot(
    x="ping_time",
    row="channel",
    figsize=(7, 7),
    vmin=-100, 
    vmax=-30,
    cmap="jet"
)


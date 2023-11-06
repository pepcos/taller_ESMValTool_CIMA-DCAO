"""Python example diagnostic."""
import logging
import os
from pathlib import Path
import glob

import xarray as xr

logger = logging.getLogger(Path(__file__).stem)


def main(cfg):

    path_hist = sorted(glob.glob("/shera/datos/CMIP/CMIP6/CMIP/NCC/NorESM2-MM/historical/r1i1p1f1/Amon/tas/gn/20191108/*.nc"))
    path_ssp = sorted(glob.glob("/shera/datos/CMIP/CMIP6/ScenarioMIP/NCC/NorESM2-MM/ssp585/r1i1p1f1/Amon/tas/gn/20191108/*.nc"))
    file_paths = path_hist+path_ssp
    ds = xr.open_mfdataset(file_paths, combine='nested', concat_dim='time').tas

    # Extract the 'DJF' months
    djf_data = ds.sel(time=ds['time.season'] == 'DJF')
    # Calculate the DJF climatology
    djf_yearly = djf_data.groupby('time.year').mean(dim='time')
    # field
    djf_climatology = djf_yearly.mean(dim="year")
    djf_climatology.plot()
    # timeseries
    djf_timeseries = djf_yearly.mean(dim=["lon", "lat"])
    djf_timeseries.plot()


if __name__ == '__main__':
    main()

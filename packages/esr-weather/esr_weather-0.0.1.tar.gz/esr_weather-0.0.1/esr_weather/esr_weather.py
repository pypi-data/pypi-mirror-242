
from datetime import datetime, timedelta
from os.path import join, basename, exists
from os import makedirs
from subprocess import call as subprocess_call
from dask.distributed import Client
import pygrib
from numpy import abs, unravel_index, argmin



BASE_GFS_URL = "https://data.rda.ucar.edu/ds084.1/{yyyy}/{yyyymmdd}/gfs.0p25.{yyyymmddhh}.f{fcst_hr}.grib2"
BASE_OBS_URL = "https://data.rda.ucar.edu/ds461.0/tarfiles/{yyyy}/gdassfcobs.{yyyymmdd}.tar.gz"


def _convert_datetime(
        analysis_start_datetime: str, 
        analysis_end_datetime: str, 
        data_type:str,
        forecast_length: int
    ) -> tuple:
    """_summary_

    Args:
        analysis_start_datetime (str): _description_
        analysis_end_datetime (str): _description_
        data_type (str): _description_
        forecast_length (int): _description_

    Raises:
        Exception: _description_

    Returns:
        tuple: _description_
    """
    analysis_start_datetime = datetime.strptime(analysis_start_datetime, "%Y%m%dT%H")
    analysis_end_datetime = datetime.strptime(analysis_end_datetime, "%Y%m%dT%H")

    if forecast_length > 0 and data_type == "obs":
        raise Exception("Forecast length is larger than 0, but your data_type is obs ...")
    
    return analysis_start_datetime, analysis_end_datetime


def _get_data_list(
        analysis_start_datetime: datetime, 
        analysis_end_datetime: datetime, 
        forecast_length: int = 0,
        start_forecast_length: int = 0,
        data_type: str = "gfs") -> list:
    """Get data list

    Args:
        analysis_start_datetime (datetime): _description_
        analysis_end_datetime (datetime): _description_
        analysis_date_interval (int): _description_
        forecast_length (int, optional): _description_. Defaults to 0.
    
    Returns:
        list: sth like [https://data.rda.ucar.edu/ds084.1/2023/20230102/gfs.0p25.2023010200.f000.grib2], 
        or ['https://data.rda.ucar.edu/ds461.0/tarfiles/2023/gdassfcobs.20230101.tar.gz']
    """

    if data_type == "gfs":
        url = BASE_GFS_URL
        proc_analysis_datetime_interval = 6
    elif data_type == "obs":
        url = BASE_OBS_URL
        proc_analysis_datetime_interval = 24
    else:
        Exception("Data type must be either gfs or obs")

    proc_analysis_datetime = analysis_start_datetime

    data_to_download = []
    while proc_analysis_datetime <= analysis_end_datetime:

        for proc_fcst_hr in range(start_forecast_length, forecast_length + 1, 3):
            data_to_download.append((
                proc_analysis_datetime + timedelta(hours=proc_fcst_hr),
                proc_analysis_datetime,
                proc_fcst_hr,
                url.format(
                    yyyy=proc_analysis_datetime.strftime("%Y"),
                    yyyymmdd=proc_analysis_datetime.strftime("%Y%m%d"),
                    yyyymmddhh=proc_analysis_datetime.strftime("%Y%m%d%H"),
                    fcst_hr=str(proc_fcst_hr).zfill(3)
            )))

        proc_analysis_datetime += timedelta(hours=proc_analysis_datetime_interval)
    
    return data_to_download


def get_nearest_data(output: dict, latlon_list: list) -> dict:
    """_summary_

    Args:
        output (dict): _description_
        latlon_list (list): _description_

    Returns:
        _type_: _description_
    """
    output["lon"] = output["lon"] % 360.0

    data = {}
    for proc_latlon in latlon_list:
        proc_lat = proc_latlon[0]
        proc_lon = proc_latlon[1]

        data[proc_latlon] = {}

        lat_diff = abs(output["lat"] - proc_lat)
        lon_diff = abs(output["lon"] - proc_lon)

        lat_index = unravel_index(argmin(lat_diff, axis=None), lat_diff.shape)
        lon_index = unravel_index(argmin(lon_diff, axis=None), lon_diff.shape)

        for proc_datetime in output["value"]:
            data[proc_latlon][proc_datetime] = {}
            for proc_field in output["value"][proc_datetime]:
                data[proc_latlon][proc_datetime][proc_field] = output[
                    "value"][proc_datetime][proc_field][lat_index[0], lon_index[1]]
    
    return data


def get_data(
    analysis_start_datetime: datetime, 
    analysis_end_datetime: datetime, 
    latlon_list: list,
    forecast_length: int = 0,
    data_archive_dir: str = "weather_data_archive",
    data_type: str = "gfs"):
    """_summary_

    Args:
        analysis_start_datetime (datetime): Analysis time (start)
        analysis_end_datetime (datetime): Analysis time (end)
        analysis_date_interval (int): Analysis hour interval (hour)
        forecast_length (int): Forecast length (Default: 0)
    """

    def _download_file(file: str):
        """Download a file

        Args:
            file (str): _description_
        """
        ofile = join(data_archive_dir, basename(file))

        if exists(ofile):
            return
        subprocess_call(["wget", "-O", f"{ofile}", file])

        return
    
    analysis_start_datetime, analysis_end_datetime = _convert_datetime(
        analysis_start_datetime, 
        analysis_end_datetime, 
        data_type,
        forecast_length
    )

    file_info = _get_data_list(
        analysis_start_datetime, 
        analysis_end_datetime, 
        forecast_length = forecast_length,
        data_type=data_type)

    if data_type == "gfs":
        # For rainfall data (we use T+12)
        file_info_for_rainfall = _get_data_list(
            analysis_start_datetime - timedelta(hours=12), 
            analysis_end_datetime - timedelta(hours=12), 
            forecast_length = 12,
            start_forecast_length = 12,
            data_type=data_type)
        file_info.extend(file_info_for_rainfall)


    if not exists(data_archive_dir):
        makedirs(data_archive_dir)


    filelist = []
    for proc_file in file_info:
        filelist.append(proc_file[-1])

    with Client(processes=False, timeout="600s") as client:
        futures = client.map(_download_file, filelist)
        client.gather(futures)

    print(f"All required files are downloaded to {data_archive_dir}")

    output = decode_gfs(file_info, data_archive_dir)

    output = get_nearest_data(output, latlon_list)

    return output


def decode_gfs(file_info: list, data_archive_dir: str, lat_range = [-50.0, -30.0], lon_range = [160.0, 180.0]):
    """Decode GFS data

    Args:
        file_info (list): _description_
        data_archive_dir (str): _description_
        lat_range (list, optional): _description_. Defaults to [-50.0, -30.0].
        lon_range (list, optional): _description_. Defaults to [160.0, 180.0].

    Returns:
        _type_: _description_
    """
    output = {}
    for proc_file in file_info:
        grbs = pygrib.open(join(data_archive_dir, basename(proc_file[-1])))

        if proc_file[0] not in output:
            output[proc_file[0]] = {}

        vars = {}
        if proc_file[2] == 0:
            vars = {}
            for proc_field in ["Temperature", "Relative humidity", "U component of wind", "V component of wind"]:
                vars[proc_field], _, _ = grbs.select(name=proc_field)[0].data(
                    lat1=lat_range[0], lat2=lat_range[1], lon1=lon_range[0], lon2=lon_range[1])
                output[proc_file[0]][proc_field] = vars[proc_field]
        elif proc_file[2] == 12:
            output[proc_file[0]]["Precipitation rate"], lats, lons  = grbs.select(name="Precipitation rate")[0].data(
                lat1=lat_range[0], lat2=lat_range[1], lon1=lon_range[0], lon2=lon_range[1])

    return {"value": output, "lat": lats, "lon": lons}

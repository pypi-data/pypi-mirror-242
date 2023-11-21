from esr_weather.esr_weather import get_data


analysis_start_datetime = "20231001T00"
analysis_end_datetime = "20231002T00"

get_data(analysis_start_datetime = analysis_start_datetime, analysis_end_datetime = analysis_end_datetime, latlon_list=[(-40.0, 175.0), (-42.0, 175.0)])
# get_data(analysis_start_datetime = analysis_start_datetime, analysis_end_datetime = analysis_end_datetime, data_type="obs")
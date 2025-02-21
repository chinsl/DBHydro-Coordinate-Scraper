# Purpose

**latlong.py** is script that takes station IDs from the [DBHydro station data access webpage](https://my.sfwmd.gov/dbhydroplsql/water_quality_interface.station_select_2?v_access_by=station&v_js_flag=Y) and downloads a csv file with the station names and associated latitude and longitude coordinates in both decimal and degrees-minutes-seconds.

# Summary

### Download Mechanism

The *fetch_coordinates* function (line 27) uses *BASE_URL*, a URL for making requests to DBHydro's database, to return station coordinates via the webscraping library *BeautifulSoup* and based on the contents of the *stations* array. It is iteratively called for each station in *stations*  (line 61), and the coordinates are stored in *station_data*, which is then converted into a dataframe (line 67). 

### Unit Conversion

The station coordinates from DBHydro are formatted in degrees-minutes-seconds by default, so they are converted to decimal via dms_to_decimal (line 88). 

### Download File

The dataframe is then converted to a csv file and saved according to the definition of *output_file* (line 95). 

Finally, The file is automatically opened using the *subprocess* library (line 91), but this can be commented out if desired.

# Instructions

### Define Station IDs

To select stations, edit the *stations* array (line 13) to include station IDs of interest:

```
stations = [
    'C44SC24', 'C44SC23', 'C44SC19', 'C44SC14', 'C44SC5', 'C44SC2', 'C44S80', 
    'C23S48', 'C24S49', 'SE+01', 'SE+02', 'SE+03', 'SE+06', 'SE+08B', 'SE+09', 'SE+11', 'SE+12', 
    'SE+13', 'S153', 'S404', 'S417E', 'S415E', 'HR1', 'GORDYRD', 'S308C'
]
```
### Define File Save Path

Edit *output_file* variable to be the appropriate save file path:

```
output_file = "/Users/metta/Documents/Research/latlong/latlong_conv_neg.csv"  # path for latlong data 
```

# Resources

The station access webpage may be found [here](https://my.sfwmd.gov/dbhydroplsql/water_quality_interface.station_select_2?v_access_by=station&v_js_flag=Y).

The DBHydro browser web page can be found [here](https://my.sfwmd.gov/dbhydroplsql/show_dbkey_info.main_menu).










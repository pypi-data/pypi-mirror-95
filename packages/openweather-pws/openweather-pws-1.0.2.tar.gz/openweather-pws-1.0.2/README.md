**Simple python wrapper around Open Weather PWS API**

## Requirements

You need API key to use it. 
You can get it for free: https://home.openweathermap.org/api_keys

## Usage

Import Station class, which contains all api methods:

    from openweather_pws import Station

#### Station

Register new station:    

    pws = Station(api_key='YOUR_API_KEY')
    station_id = pws.register(external_id='YOUR_STATION_EXTERNAL_ID', 
                              name='YOUR STATION LONG NAME', 
                              latitude='44.419181',
                              longitude='38.205109', 
                              altitude='70') # altitude in meters
    # If you plan to use pws class further, please note that 
    # station_id will be stored as default station_id of class.
    # Note: always use different external_id for each station! 
    
Get info about the station:

    pws = Station(api_key=api_key)
    pws.info(station_id='YOUR_STATION_ID')
    
Or, when `station_id` is set:

    pws = Station(api_key=api_key, station_id='YOUR_STATION_ID')
    # if you iniatilize Station class with station_id param, 
    # it will be used as default in all API call, if another is not specified

You can set/change `station_id` any time you want:

    pws.set_station_id(station_id)

Update station info:

    pws.update(station_id, external_id, name, latitude, longitude, altitude)
    
Delete station:
    
    pws.delete(station_id)
    
Get all stations info

    pws.all_stations() # will return all stations registered by user in list
    
#### Measurements

Measurements can be accessed via Station class:

    pws.measurements.%method% 
 
or directly, if needed:

    from openweather_pws import Measurements
   
    meas = Measurements(api_key='YOUR_API_KEY', station_id='YOUR_STATION_ID')  # station_is optional

Also, you can set/change `station_id` any time you want:

    meas.set_station_id(station_id) 

To obtain list of measurements from station:

    measurements = pws.meas.get(station_id, meas_type, limit, time_from, time_to)
    # all params are optional
    # by default will be used default station_id, hourly data (24 measurements)
    # refer to: https://openweathermap.org/stations#get_measurements
    
Get only one measurement:

    measurement = pws.meas.get_one(station_id, meas_type, time_from, time_to)
    # all params are optional
    # by default will be used default station_id and hourly data, 1 measurement


Send data of one measurement to PWS:

    pws.meas.set(dt, station_id, temperature, wind_speed, wind_gust, wind_deg,
            pressure, humidity, rain_1h, rain_6h, rain_24h, snow_1h, snow_6h,
            snow_24h, dew_point, humidex, heat_index, visibility_distance,
            visibility_prefix, clouds, weather)
    # all params are optional
    # by default will be used default station_id, dt is current time in unixtime format
    # refer to: https://openweathermap.org/stations#measurement
    
Send bulk data of PWS you'll need to prepare list with dicts and send it via:

    pws.meas.set_bulk(payload)
    
## Terms of service

Refer to 
https://openweathermap.org/

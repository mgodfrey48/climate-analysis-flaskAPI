# Imports
from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import numpy as np
import datetime as dt

############ Database Setup ############

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
Stations = Base.classes.station


############ Flask setup ############
# Create the app
app = Flask(__name__)



############ Flask routes ############
# Homepage - list all routes available
@app.route("/")
def home():
    return (
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/<start> <br/>"
        f"/api/v1.0/<start>/<end>"
    )

# Precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create the session from python to the database
    session = Session(engine)

    # Query database for date and precipitation data
    results = session.query(measurement.date, measurement.prcp).all()

    # Close the session
    session.close()

    # Create a dictionary for the row data and return a jsonified version of it
    precip_data = []
    for date, prcp in results:
        precipitation = {}
        precipitation["date"] = date
        precipitation["precipitation"] = prcp
        precip_data.append(precipitation)

    return jsonify(precip_data)

# Stations
@app.route("/api/v1.0/stations")
def stations():
    # Create the session from python to the database
    session = Session(engine)

    # Query database for station data
    station_results = session.query(Stations.station, Stations.name).all()

    # Close the session
    session.close()

    # Convert the list of tuples into a normal list
    stations = []
    for station, name in station_results:
        station_info = {}
        station_info["Station"] = station
        station_info["Name"] = name
        stations.append(station_info)

    # Return a json list of the stations
    return jsonify(stations)

# Temperature observations
@app.route("/api/v1.0/tobs")
def temp_observations():
    # Create the session from python to the database
    session = Session(engine)

    # Query database for station data
    first_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    station_results = session.query(measurement.date, measurement.tobs).filter((measurement.station == func.max(measurement.station)) & (measurement.date > first_date))

    # Close the session
    session.close()

    # Create the list of temperatures from the last year
    temperatures = []
    for tobs in station_results:
        temperatures.append(tobs)

    # Return a json list of the temperatures
    return jsonify(temperatures)

# Temperature calculations



if __name__ == "__main__":
    app.run(debug=True)
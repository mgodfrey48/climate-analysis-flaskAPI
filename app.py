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
        f"/api/v1.0/precipitation  --> Returns precipitation data for every recorded observation<br/>"
        f"/api/v1.0/stations  --> Returns the names of every station<br/>"
        f"/api/v1.0/tobs  --> Returns a list of temperatures from the last year of recorded data for the most active weather station<br/>"
        f"/api/v1.0/YYYY-MM-DD  --> Returns the min, max. and average temperatures after a given start date (entered using the YEAR-MONTH-DAY format) <br/>"
        f"/api/v1.0/YYYY-MM-DD/YYYY-MM-DD  --> Returns the min, max. and average temperatures between a given start and end date (entered using the YEAR-MONTH-DAY format)"
    )


# Precipitation data
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create the session from python to the database
    session = Session(engine)

    # Query database for date and precipitation data
    results = session.query(measurement.date, measurement.prcp).all()

    # Close the session
    session.close()

    # Create a dictionary for the row data and return a jsonified version of it
    precip_data = {date: prcp for date, prcp in results}
    return jsonify(precip_data)

# Station names
@app.route("/api/v1.0/stations")
def stations():
    # Create the session from python to the database
    session = Session(engine)

    # Query database for station data
    station_results = session.query(Stations.station, Stations.name).all()

    # Close the session
    session.close()

    # Convert stations into a normal list
    stations = list(np.ravel(station_results))

    # Return a json list of the stations
    return jsonify(stations)


# Temperature observations for the last year of available data
@app.route("/api/v1.0/tobs")
def temp_observations():
    # Create the session from python to the database
    session = Session(engine)

    # Query the database for temperature observations from the most active station for the last year of data
    first_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    station_results = session.query(measurement.tobs).filter((measurement.date > first_date) & (measurement.station == 'USC00519281'))

    # Close the session
    session.close()

    # Create the list of temperatures from the last year
    temperatures = []
    for tobs in station_results:
        temperatures.append(tobs)

    temperatures = list(np.ravel(temperatures))
    
    # Return a json list of the temperatures
    return jsonify(temperatures)


# Temperature calculations after a specific start date
@app.route("/api/v1.0/<start>")
def tobs_by_date(start):
    # Create the session from python to the database
    session = Session(engine)

    # Query database for temperature observations after the date given by the user
    temps = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date >= start)

    # Close the session
    session.close()

    # Return the temperature data
    temp_data = []
    for min, max, avg in temps:
        info = {}
        info["min"] = min
        info["max"] = max
        info["Avg"] = avg
        temp_data.append(info)
    return jsonify(temp_data)


# Temperature calculations between specific start and end dates
@app.route("/api/v1.0/<start>/<end>")
def tobs_between_dates(start, end):
    # Create the session from python to the database
    session = Session(engine)

    # Query database for temperature observations after the date given by the user
    temps = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter((measurement.date >= start) & (measurement.date <= end))

    # Close the session
    session.close()

    # Return the temperature data
    temp_data = []
    for min, max, avg in temps:
        info = {}
        info["min"] = min
        info["max"] = max
        info["Avg"] = avg
        temp_data.append(info)    
    return jsonify(temp_data)



if __name__ == "__main__":
    app.run(debug=True)
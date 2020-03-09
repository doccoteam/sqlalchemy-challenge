#dependencies

import datetime as dt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

@app.route("/")

def home():
    print("'Home' page")
    return "Surfs Up Weather API"



@app.route("/welcome")
def welcome():
    return(
    f"Welcome to the Surf Up API<br>"
    f"Available Routes:<br>"
    f"/api/v1.0/precipitation<br>"
    f"/api/v1.0/stations<br>"
    f"/api/v1.0/tobs<br>"
    f"/api/v1.0/<start><br>"
    f"/api/v1.0<start>/<end><br>"
    )

@app.route("/api/v1.0/precipitation")

def precipitation():

#Query for the dates and temperature observations from the last year.

    results = session.query(Measurements.date,Measurements.prcp).filter(Measurements.date >= "08-23-2017").all()
    prcp = list(np.ravel(results))

#results.___dict___
#Create a dictionary using 'date' as the key and 'prcp' as the value.

    """prcp = []
    for result in results:
        row = {}
        row[Measurements.date] = row[Measurements.prcp]
        prcp.append(row)"""

    return jsonify(prcp)

@app.route("/api/v1.0/stations")

def stations():

#return a json list of stations from the dataset.
    results = session.query(Stations.station).all()
    stations = list(np.ravel(results))

    return jsonify(stations)

@app.route("/api/v1.0/tobs")

def temperature():

#Return a json list of Temperature Observations (tobs) for the previous year

    tobs = []
    results = session.query(Measurements.tobs).filter(Measurements.date >= "08-23-2017").all()
    tobs = list(np.ravel(results))
    return jsonify(tobs)


@app.route("/api/v1.0/<start>")
def start_vacation_temp(start_date):
    start_vac = []
    temp_min = session.query(func.min(Measurements.tobs)).filter(Measurements.date == start_date).all()
    temp_max = session.query(func.max(Measurements.tobs)).filter(Measurements.date == start_date).all()
    temp_avg = session.query(func.avg(Measurements.tobs)).filter(Measurements.date == start_date).all()
    start_vac = list(np.ravel(temp_min,temp_max,temp_avg))
    return jsonify(start_vac)

def after_start_date(start_date):
    start_vac_date_temps = []
    temp_min = session.query(func.min(Measurements.tobs)).filter(Measurements.date >= start_date).all()
    temp_max = session.query(func.max(Measurements.tobs)).filter(Measurements.date >= start_date).all()
    temp_avg = session.query(func.avg(Measurements.tobs)).filter(Measurements.date >= start_date).all()
    start_vac_date_temps = list(np.ravel(temp_min,temp_max,temp_avg))
    return jsonify(start_vac_date_temps)

@app.route("/api/v1.0/<start>/<end>")
def start_end_vacation(start_date, end_date):
    start_end_vac_temps = []
    temp_min = session.query(func.min(Measurements.tobs)).\
    filter(Measurements.date == start_date, Measurements.date == end_date).all()
    temp_max = session.query(func.max(Measurements.tobs)).filter(Measurements.date == start_date, Measurements.date == end_date).all()
    temp_avg = session.query(func.avg(Measurements.tobs)).filter(Measurements.date == start_date, Measurements.date == end_date).all()
    start_end_vac_temps = list(np.ravel(temp_min,temp_max,temp_avg))
    return jsonify(start_end_vac_temps)

def start_end_vac(start_date, end_date):
    vac_temps = []
    temp_min = session.query(func.min(Measurements.tobs)).filter(Measurements.date >= start_date, Measurements.date >= end_date).all()
    temp_max = session.query(func.max(Measurements.tobs)).filter(Measurements.date >= start_date, Measurements.date >= end_date).all()
    temp_avg = session.query(func.avg(Measurements.tobs)).filter(Measurements.date >= start_date, Measurements.date >= end_date).all()
    vac_temps = list(np.ravel(temp_min,temp_max,temp_avg))
    return jsonify(vac_temps)

if __name__ == '__main__':
    app.run(debug=True)    